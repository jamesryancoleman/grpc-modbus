from modbus_parser import ModbusParams
import datetime as dt
import comms_pb2
import client

# functions
READ_REGISTER = "read-register"
READ_MULTIPLE_REGISTERS = "read-registers"
WRITE_REGISTER = "write-register"
# test parameters
SERVER_ADDR = "nuc:50063"

host_1 = "192.168.13.144"   # change this to the right IP address
function_1 = READ_MULTIPLE_REGISTERS
function_2 = WRITE_REGISTER

address_1 = "16386" # voltage
address_2 = "16402" # current
address_3 = "4104" # CT1 (current transformer)
address_4 = "4105" # CT2 (current transformer)

port_number = "502"

# port_number = "502"

# read urls for testing
URL_1 = "modbus://192.168.13.3:502/read-registers/?type=f"
# URL_2 = "modbus://192.168.13.3:502/write-registers/?type=f&value=20"

url_1 = "modbus://{}:{}/{}/{}?type=f".format(host_1, port_number, function_1, address_1)
url_2 = "modbus://{}:{}/{}/{}?type=f".format(host_1, port_number, function_1, address_2)
url_3 = "modbus://{}:{}/{}/{}?type=h".format(host_1, port_number, function_2, address_3) # &value=20
url_4 = "modbus://{}:{}/{}/{}?type=h".format(host_1, port_number, function_2, address_4) # &value=333
full_url_list = [url_1, url_2, url_3, url_4]
read_tests = [url_1, url_2]
write_tests = [url_3, url_4]
write_values = ["20", "333"]

def get_test(key:list[str]):
    print("== started get test ==")
    start = dt.datetime.now()
    pairs = client.Get(key, addr=SERVER_ADDR)
    end = dt.datetime.now()
    completed_in = end-start
    for p in pairs:
        print("\t{} -> '{}'".format(p.Key, p.Value))
    print("== get test completed in {} ==".format(completed_in))

def set_test(keys:list[str], values: list[str]):
    print("== started set test ==")
    start = dt.datetime.now()
    pairs = []
    for i in range(len(keys)):
        pair = comms_pb2.SetPair(Key=write_tests[i], Value=write_values[i], Ok = False)
        pairs.append(pair)
    pairs = client.Set(pairs, SERVER_ADDR)
    end = dt.datetime.now()
    completed_in = end-start
    for p in pairs:
        ok = "failed to write"
        if p.Ok:
            ok = "ok"
        print("\t{} -> '{}' ({})".format(p.Key, p.Value, ok))
    print("== set test completed in {} ==".format(completed_in))

# TODO compile a regex with named matches to extract the parameters needed by 
# py-modbus to get the actual value.
# probably something like
# modbus_regex = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<func>[a-zA-Z-_.,]+)?/(?P<address>[0-9]+)\?type=?P<type>[fH]')
modbus_pattern = r"^modbus://(?P<host>[a-zA-Z0-9.-]+):(?P<port>[0-9]+)/(?P<function>[a-zA-Z-]+)/(?P<address>[0-9]+)/\?type=(?P<type>[a-zA-Z]+)&value=(?P<value>[0-9]+)"
if __name__ == "__main__":
    # test the parser
    for url in full_url_list:
        print("== Testing params parser ==")
        params = ModbusParams(url)
        params.PrintParams()
        print("== completed params parser test ==")

    # test Get()
    """
    get_test(read_tests)

    """
    #test Set()
    set_test(write_tests, write_values)
    # make sure read the values you set 
    get_test(write_tests)
