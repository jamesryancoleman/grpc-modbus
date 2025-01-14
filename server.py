#!/usr/bin/env python3
"""
A gRPC server to handle modbus work.

"""
import asyncio
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
import comms_pb2
import comms_pb2_grpc
import logging
from enum import Enum
from typing import Union

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
        
def write_register(client: ModbusTcpClient, address: str, value: str) -> Union[str, None]:
    """
    Writes a register from a Modbus device using a Modbus TCP client.

    This function sends a write request ot the Modbus device specified by the 
    `client` parameter and writes the value to a specified register. 

    Parameters:
        client (ModbusTcpClient): An instance of ModbusTcpClient used to 
                                  communicate with the Modbus device.
        address (str): The address on the Modbus device to write to.
        value(str): The value to write to at the specified address on the Modbus device.

    Returns a string representation of the response (ex. WriteMultipleRegisterResponse (4104,1))
    """
    response = None
    try:
        response = client.write_registers(address=int(address), values=int(value), slave=1)
        print("Response is: ", response)
    except ModbusException as exc:
        print(f"Modbus exception: {exc!s}")
        error = True
            
    return(str(response)) # return response or None

def read_register(client: ModbusTcpClient, type_param: str, address: str) -> None:
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
    data_type = get_data_type(type_param) # format is the char representing the data type
    count = data_type.value[1] # this is the number of bytes to read
    _logger.info(f"*** Reading {count} bytes")
    var_type = data_type.name
    _logger.info(f"*** Reading ({var_type})")
    rr = None
    try: # NOT SURE SLAVE IS NEEDED BUT NEED TO TEST -- THINK COUNT NEEDS TO BE reg_nb=count
        rr = client.read_holding_registers(address=int(address), count=count, slave=1)
    except ModbusException as exc:
        _logger.error(f"Modbus exception: {exc!s}")
        error = True
        if rr.isError():
            _logger.error(f"Error")
            error = True
        if isinstance(rr, ExceptionResponse):
            _logger.error(f"Response exception: {rr!s}")
            error = True

    _logger.info(f"*** READ *** of address {address} = {rr}")
    value = client.convert_from_registers(rr.registers, data_type) # took out the *factor, but can add it in later
    if value is None:
        value = "None"
    return value

# TODO: GetMultiple becomes Get, Set Multiple becomes Set. Remove old get and set.
# Get now takes keys, a []str, and returns a GetResponse with field Pairs, as list of GetPairs.
# For each key in keys, return a comms.GetPair(Key=k, Value=v, Error=None|err).
# Set now takes a list of SetPairs(key, value)
# Set now returns a list of SetPair with the Ok field set to True if it worked,
# or False if it failed.
class modbusRPCServer(comms_pb2_grpc.GetSetRunServicer): 
    """
    A gRPC server implementation for handling Modbus RPC requests.

    This class extends the GetSetRunServicer provided by the comms_pb2_grpc module,
    implementing methods to facilitate Modbus communication over gRPC. It serves as 
    the interface for clients to perform read and write operations on Modbus devices.
    
    Methods:
        Get(request: comms_pb2.GetRequest, context): 
            Handles requests to read data from a Modbus device.
        
        Set(request: comms_pb2.SetRequest, context): 
            Handles requests to write data to a Modbus device.
    """

    def Get(self, request:comms_pb2.GetRequest, context):
        logging.info('received Get request: ', request)

        header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        pairs = []

        # loop over all keys in the request.Keys list
        for key in request.Keys:
            # parse the params
            params = MODbusParams(key)

            # create and connect to the client
            client: ModbusTcpClient = ModbusTcpClient(
            host=params.host,
            port=params.port,
            framer=FramerType.SOCKET,
            timeout=5,
            )
            client.connect()
            _logger.info("### Client connected")
            sleep(1)
            # read the register
            value = read_register(client, params.type_param, params.address)
            if value is None:
                value = "Nothing"
            # form the GetPair
            pair = comms_pb2.GetPair(
                Key=key,
                Value = str(value)
            )
            # add GetPair to the list of pairs to return 
            pairs.append(pair)

            # close the client
            client.close()

        _logger.info("### End of Get -> Now Making the GetResponse")

        # change the GetResponse
        return comms_pb2.GetResponse(
            Header=header,
            Pairs=pairs,
        )

    def Set(self, request:comms_pb2.SetRequest, context):
        header = comms_pb2.Header(Src=request.Header.Src, Dst=request.Header.Dst)
        logging.info('received Set request: ', request)
        pairs = []
        # loop over all key-value pairs
        for pair in request.Pairs:
            Ok = False
            # parse the params
            params = MODbusParams(pair.Key)
            params.PrintParams()

            # create and connect to the client
            client: ModbusTcpClient = ModbusTcpClient(
            host=params.host,
            port=params.port,
            framer=FramerType.SOCKET,
            timeout=5,
            )
            client.connect()
            _logger.info("### Client connected")
            sleep(1)

            # write to the register
            response_value = write_register(client, params.address, pair.Value)
        
            if response_value:
                Ok = True
            # construct pair and add it to the list
            pair = comms_pb2.SetPair(Key=pair.Key, Value=response_value, Ok=Ok)
            pairs.append(pair)

        return comms_pb2.SetResponse(
            Header = header,
            Pairs=pairs
        )

# need to use specified port in the oxigraph instance
async def serve(port:str="50062") -> None:
    # GRPC set up
    server = grpc.aio.server()
    comms_pb2_grpc.add_GetSetRunServicer_to_server(modbusRPCServer(), server)
    server.add_insecure_port("[::]:" + port)
    logging.info("Server started. Listening on port: %s", port)
    await server.start()
    # server.wait_for_termination()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown")
        await server.stop(5)
    
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(serve())
    finally:
        loop.close()