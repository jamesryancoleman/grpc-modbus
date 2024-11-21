#!/usr/bin/env python3
"""Pymodbus Synchronous Client Example.
Modified to test long term connection.
Modified to actually work with Huawei SUN2000 inverters, that better support async Modbus operations so errors will occur
Configure HOST (the IP address of the inverter as a string), PORT and CYCLES to fit your needs
"""
import logging
from enum import Enum
from math import log10
from time import sleep
from pymodbus import pymodbus_apply_logging_config
# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus import FramerType
HOST = "192.168.13.3"
PORT = 502
CYCLES = 1

pymodbus_apply_logging_config(logging.ERROR)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)

def main() -> None:
    """Run client setup."""
    _logger.info("### Client starting")
    # choose the TCP client
    client: ModbusTcpClient = ModbusTcpClient(
        host=HOST,
        port=PORT,
        # Common optional parameters:
        framer=FramerType.SOCKET,
        timeout=5,
    )
    client.connect()
    _logger.info("### Client connected")
    sleep(1)
    _logger.info("### Client starting")
    write_register(client)
    for count in range(CYCLES):
        _logger.info(f"Running loop {count}")
        meter_calls(client)
        sleep(5)  # scan interval
    client.close()
    _logger.info("### End of Program")
# TODO this doesn't work
def write_register(client: ModbusTcpClient) -> None:
    """Write a register."""
    error = False
    try:
        result = client.read_holding_registers(4105, count=1)
        _logger.info(f"read is {result}")
        if result.isError():
            _logger.error(f"Error with the read")
        
    except ModbusException as exc:
        _logger.error(f"Modbus exception with read is : {exc!s}")
        error = True

    try:
        rr1 = client.write_registers(address=4104, values=20, slave=1)
        rr = client.write_registers(address=4105, values=333, slave=1)

        _logger.info(f"write is {rr}")
        _logger.info(f"write is {rr1}")

    except ModbusException as exc:
        _logger.error(f"Modbus exception: {exc!s}")
        error = True
    if rr.isError():
        _logger.error(f"Error")
        error = True
    if isinstance(rr, ExceptionResponse):
        _logger.error(f"Response exception: {rr!s}")
        error = True
def meter_calls(client: ModbusTcpClient) -> None:
    """Read registers."""
    error = False
    # what is factor for??
    for addr, format, factor, comment, unit in ( # data_type according to ModbusClientMixin.DATATYPE.value[0]
        (16384, "f", 1,     "freq_1",    "Hz"),
        (16386, "f", 1,     "voltage",   "V"),
        (16412, "f", 20,    "power",     "W"),
        (16402, "f", 20,    "current",   "A"),
        (4104, "h", 1,    "CT1",   "Not sure"),
        (4105, "h", 1,    "CT2",   "Not sure"),
        (4101, "f", 1,    "PT1",   "Not sure"),
        (4102, "f", 1,    "PT2-1",   "Not sure"),
        (4103, "f", 1,    "PT2-2",   "Not sure"),
    ):
        if error:
            error = False
            client.close()
            sleep(0.1)
            client.connect()
            sleep(1)
        
        data_type = get_data_type(format)
        _logger.info(f"data_type is {data_type}")
        count = data_type.value[1] # this is the number of bytes to read
        _logger.info(f"count is {count}")
        var_type = data_type.name
        _logger.info(f"*** Reading {comment} ({var_type})")
        
        try:
            rr = client.read_holding_registers(address=addr, count=count, slave=1)

        except ModbusException as exc:
            _logger.error(f"Modbus exception: {exc!s}")
            error = True
            continue
        if rr.isError():
            _logger.error(f"Error")
            error = True
            continue
        if isinstance(rr, ExceptionResponse):
            _logger.error(f"Response exception: {rr!s}")
            error = True
            continue

        # what is factor?
        value = client.convert_from_registers(rr.registers, data_type) * factor

        # for small values, use a log scale to pick number of decimal places
        if factor < 1:
            value = round(value, int(log10(factor) * -1))
        
        _logger.info(f"*** READ *** {comment} = {value} {unit}")

def get_data_type(format: str) -> Enum:
    """Return the ModbusTcpClient.DATATYPE according to the format"""
    for data_type in ModbusTcpClient.DATATYPE:
        if data_type.value[0] == format:
            return data_type
if __name__ == "__main__":
    main()


