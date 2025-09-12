import unittest
import logging

import asyncio
import grpc

from pymodbus.client import ModbusTcpClient
from pymodbus import FramerType

import src.common_pb2_grpc as common_pb2_grpc
import src.common_pb2 as common_pb2
from src.server import serve

class TestServer(unittest.TestCase):
    def setUp(self):
        # Code to be tested
        self.logger = logging.getLogger('my_app_logger')
        logging.basicConfig(level=logging.DEBUG)

        """ these addresses must be live and on your network
        """
        self.uri_tests = [
            "modbus://192.168.13.164:502/read-registers/16384?type=f",
            "modbus://192.168.13.164:502/read-registers/16386?type=f",
            "modbus://192.168.13.164:502/read-registers/16402?type=f",
            "modbus://192.168.13.164:502/read-registers/16412?type=f",
        ]
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()
    
    async def _async_test_method(self):
        # Start the server and get the server object
        port = "60053" # non standard port for testing
        self.server = await serve(port=port)

        self.logger.debug("not blocked by await serve")
                
        try:
            # Wait for the server to be ready
            await asyncio.sleep(1)
            
            # Use the client to interact with the server
            async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
                
                stub = common_pb2_grpc.DeviceControlStub(channel)
                
                get_request = common_pb2.GetRequest(
                    Keys=self.uri_tests
                )

                # run a Get call
                response:common_pb2.GetResponse = await stub.Get(get_request)

                for pair in response.Pairs:
                    print(pair.Key, "->", pair.Value)

                #TODO: write some tests
                # self.assertSomething(response)

        finally:
            # Gracefully shut down the server
            await self.server.stop(5)
            await self.server.wait_for_termination()


    def test_server(self):
        # Run the async test method
        self.loop.run_until_complete(self._async_test_method())

