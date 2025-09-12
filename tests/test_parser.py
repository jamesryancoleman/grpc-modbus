import unittest

from src.modbus_parser import ModbusParams

class TestParser(unittest.TestCase):
    def setUp(self):
        self.uri_tests = [
            "modbus://192.168.13.154:502/read-registers/16384?type=f",
            "modbus://192.168.13.154:502/read-registers/16386?type=f",
            "modbus://192.168.13.154:502/read-registers/16402?type=f",
            "modbus://192.168.13.154:502/read-registers/16412?type=f",
        ]

    def test_parser(self):
        for u in self.uri_tests:
            params = ModbusParams(u)
            print(f"{u} ->")
            params.PrintParams()
            print()
