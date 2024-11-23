import sys
import grpc
import device_pb2
import device_pb2_grpc

# device_address = "192.168.13.3"
# description = "Power Monitor"

"""Usage:
    client sends a uri that identifies point it would like to access.

    e.g., ""modbus://192.168.13.3/502/read-registers/16386?type=f"
    
"""

def Get(key:str, addr="localhost:50062") -> str:
    header = device_pb2.Header(Src="localhost:2822", Dst=addr)

    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        result:device_pb2.GetResponse
        result = stub.Get(device_pb2.GetRequest(
            Header=header,
            Key=key,
        ))
        return result.Value
    

def GetMultiple(keys:list[str], addr="localhost:50062") -> list[device_pb2.GetResponse]:
    header = device_pb2.Header(Src="localhost:2822", Dst=addr)
    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        result:device_pb2.GetMultipleResponse
        result = stub.GetMultiple(device_pb2.GetMultipleRequest(
            Header=header,
            Keys=keys
        ))
    
    return result.Responses

def Set(key:str, value:str, addr="localhost:50062") -> device_pb2.SetResponse:
    header = device_pb2.Header(Src="localhost:2822")
    
    result:device_pb2.SetResponse

    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)

        result = stub.Get(device_pb2.SetRequest(
            Header=header,
            Key=key,
            Value=value, 
        ))
    
    return result
if __name__=="__main__":
    pass