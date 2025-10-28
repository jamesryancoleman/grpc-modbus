import unittest

from pymodbus.client import ModbusTcpClient
from pymodbus import FramerType

from src.modbus_parser import ModbusParams
from src.server import read_register

class TestParser(unittest.TestCase):
    def setUp(self):
        """ these addresses must be live and on your network
        """
        self.uri_tests = [
            "modbus://192.168.13.164:502/read-registers/16384?type=f",
            "modbus://192.168.13.164:502/read-registers/16386?type=f",
            "modbus://192.168.13.164:502/read-registers/16402?type=f",
            "modbus://192.168.13.164:502/read-registers/16412?type=f",
        ]

    def test_read(self):
        for u in self.uri_tests:
            params = ModbusParams(u)
            print(f"{u} ->")
            params.PrintParams()
            print()

            # create and connect to the client
            client: ModbusTcpClient = ModbusTcpClient(
                host=params.host,
                port=params.port,
                framer=FramerType.SOCKET,
                timeout=5,
            )
            client.connect()
            value = read_register(client, params.type_param, params.address)
            print(f"{u} == {value}")

            # close the client
            client.close()

    def test_write(self):
        pass
