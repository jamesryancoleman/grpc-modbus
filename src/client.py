import sys
import grpc
import common_pb2
import common_pb2_grpc

# device_address = "192.168.13.3"
# description = "Power Monitor"

"""Usage:
    client sends a uri that identifies point it would like to access.

    e.g., ""modbus://192.168.13.3/502/read-registers/16386?type=f"
    
"""

def Get(keys:list[str], addr="localhost:50062") -> list[common_pb2.GetPair]:
    header = common_pb2.Header(Src="localhost:2822", Dst=addr)

    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.GetSetRunStub(channel)
        result:common_pb2.GetResponse
        request = common_pb2.GetRequest(
            Header=header,
            Keys=keys,
        )
        # print(request)
        result = stub.Get(request)
    return result.Pairs


def Set(pairs:list[common_pb2.SetPair], addr="localhost:50062") -> list[common_pb2.SetPair]:
    header = common_pb2.Header(Src="localhost:2822")
    
    result:common_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.GetSetRunStub(channel)

        result = stub.Set(common_pb2.SetRequest(
            Header=header,
            Pairs=pairs,
        ))
    
    return result.Pairs
if __name__=="__main__":
    pass