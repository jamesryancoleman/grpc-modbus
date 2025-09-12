# grpc-modbus

This project demonstrates how to expose modbus TCP/IP data to a network via `Get` and `Set` gRPC interfaces.

The `key` of a request is expected to be of the format:
`modbus://{device_address}:{port}/read-registers/{address}?type=f`.

## Common files
Implmenting a driver requires implementing the `Get` and `Set` methods of the `DeviceControl` service.

- `common.proto` includes the definition of the DeviceControl service in the Protocol Buffer language.
- `common_pb2_grpc.py` provides the server stubs to extend.
- `common_pb2.pyi` provices the messages classes used for requests and responses.

