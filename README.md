# grpc-modbus

This project demonstrates how to expose modbus TCP/IP data to a network via `Get` and `Set` gRPC interfaces.

The `key` of a request is expected to be of the format:
`modbus://{device_address}:{port}/read-registers/{address}?type=f`.

## Common files
Implmenting a driver requires implementing the `Get` and `Set` methods of the `DeviceControl` service.

- `common.proto` for references. Defines the DeviceControl service and its requirement methods in the Protocol Buffer language.
- `src/common_pb2_grpc.py` provides the server stubs to extend.
- `src/common_pb2.pyi` provices the messages classes used for requests and responses.

### Testing
To run tests don't forget to activate venv: e.g., `source ./venv/bin/activate`

#### Example
To run a specific test try something like:
`python -m unittest -v tests.test_server`

Output should look like:
``` shell
...
modbus://{ip}:502/read-registers/16384?type=f -> 59.944000244140625
modbus://{ip}:502/read-registers/16386?type=f -> 118.87457275390625
modbus://{ip}:502/read-registers/16402?type=f -> 0.020628824830055237
modbus://{ip}:502/read-registers/16412?type=f -> 0.9188230037689209
ok

----------------------------------------------------------------------
Ran 1 test in 1.396s
```