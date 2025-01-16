import sys
import grpc
import comms_pb2
import comms_pb2_grpc

# device_address = "192.168.13.3"
# description = "Power Monitor"

"""Usage:
    client sends a uri that identifies point it would like to access.

    e.g., ""modbus://192.168.13.3/502/read-registers/16386?type=f"
    
"""

def Get(key:[str], addr="localhost:50062") -> str:
    header = comms_pb2.Header(Src="localhost:2822", Dst=addr)

    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        result:comms_pb2.GetResponse
        result = stub.Get(comms_pb2.GetRequest(
            Header=header,
            Keys=key,
        ))
        return result.Pairs


def Set(key:str, addr="localhost:50062") -> comms_pb2.SetResponse:
    header = comms_pb2.Header(Src="localhost:2822")
    
    result:comms_pb2.SetResponse

    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)

        result = stub.Set(comms_pb2.SetRequest(
            Header=header,
            Key=key,
        ))
    
    return result
if __name__=="__main__":
    pass