#!/usr/bin/env python3
"""
A gRPC server to handle modbus work.

"""
from modbus_parser import MODbusParams
from pymodbus import pymodbus_apply_logging_config
# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus import FramerType
from time import sleep
import grpc
import device_pb2
import device_pb2_grpc
import logging
from enum import Enum

pymodbus_apply_logging_config(logging.ERROR)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)


def get_data_type(format: str) -> Enum:
    """
    Return the ModbusTcpClient.DATATYPE according to the format
    
    Parameters:
        format (str): The type of data being read from the register (ex. h, f, etc)
    """
    for data_type in ModbusTcpClient.DATATYPE:
        if data_type.value[0] == format:
            return data_type

def read_register(client: ModbusTcpClient) -> None:
    """
    Reads a register from a Modbus device using a Modbus TCP client.

    This function sends a read request to the Modbus device specified by the 
    `client` parameter and retrieves data from a specified register. The 
    register and the data it contains are typically defined by the device's 
    Modbus protocol configuration.

    Parameters:
        client (ModbusTcpClient): An instance of ModbusTcpClient used to 
                                  communicate with the Modbus device.

    Returns:
        None
    """
    data_type = get_data_type(format)
    _logger.info(f"data_type is {data_type}")
    count = data_type.value[1] # this is the number of bytes to read
    _logger.info(f"count is {count}")
    var_type = data_type.name
    _logger.info(f"*** Reading ({var_type})")
    count = 1
    try: # NOT SURE SLAVE IS NEEDED BUT NEED TO TEST -- THINK COUNT NEEDS TO BE reg_nb=count
        rr = client.read_holding_registers(address=client.address, count=count, slave=1)

    except ModbusException as exc:
        _logger.error(f"Modbus exception: {exc!s}")
        error = True
    if rr.isError():
        _logger.error(f"Error")
        error = True
    if isinstance(rr, ExceptionResponse):
        _logger.error(f"Response exception: {rr!s}")
        error = True

    _logger.info(f"*** READ *** of address {client.address} = {value}")

    value = client.convert_from_registers(rr.registers, data_type) # took out the *factor, but can add it in later
    
    return value

def write_register():
    pass

class modbusRPCServer(device_pb2_grpc.GetSetRunServicer): 
    """
    A gRPC server implementation for handling Modbus RPC requests.

    This class extends the GetSetRunServicer provided by the device_pb2_grpc module,
    implementing methods to facilitate Modbus communication over gRPC. It serves as 
    the interface for clients to perform read and write operations on Modbus devices.
    
    Methods:
        Get(request: device_pb2.GetRequest, context): 
            Handles requests to read data from a Modbus device.
        
        Set(request: device_pb2.SetRequest, context): 
            Handles requests to write data to a Modbus device.
        
        GetMultiple(request: device_pb2.GetMultipleRequest, context): 
            Handles requests to read multiple data points from a Modbus device.
        
        SetMultiple(request: device_pb2.SetMultipleRequest, context): 
            Handles requests to write multiple data points to a Modbus device.
    """

    def Get(self, request:device_pb2.GetRequest, context):
        logging.info('received Get request: ', request)

        header = device_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        # parse the params
        print("request key is ", request.Key)
        params = MODbusParams(request.Key)

        # create and connect to the client
        client: ModbusTcpClient = ModbusTcpClient(
        host=params.host,
        port=params.port,
        # Common optional parameters: NOT INCLUDED RN
        framer=FramerType.SOCKET,
        timeout=5,
        )
        client.connect()
        _logger.info("### Client connected")
        sleep(1)

        # read the register
        value = read_register(client)

        # close the client and return the response -- ERROR HANDLING???
        client.close()

        _logger.info("### End of Get -> Now Making the GetResponse")
        return device_pb2.GetResponse(
            Header=header,
            Key=request.Key,
            Value=str(value)
        )


    def GetMultiple(self, request:device_pb2.GetMultipleRequest, context):
        header = device_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        # want to test Get before I do GetMultiple()
        # will problably be a loop with some weird figuring out of results

    def Set(self, request:device_pb2.SetRequest, context):
        header = device_pb2.Header(Src=request.Header.Src, Dst=request.Header.Dst)
    def SetMultiple(self, request:device_pb2.SetMultipleRequest, context):
        header = device_pb2.Header(Src=request.Header.Src, Dst=request.Header.Dst)
