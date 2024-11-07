from modbus_parser import MODbusParams
import client
# functions
READ_REGISTER = "read-register"
READ_MULTIPLE_REGISTERS = "read-registers"

# test parameters
host_1 = "192.168.13.3"   # change this to the right IP address
function_1 = READ_MULTIPLE_REGISTERS

address_1 = "16386" # voltage
address_2 = "16402" # current

port_number = "502"

port_number = "502"

# read urls for testing
URL_1 = "modbus://192.168.13.3/502/read-registers/16386?type=f"
url_1 = "modbus://{}/{}/{}/{}?type=f".format(host_1, port_number, function_1, address_1)
url_2 = "modbus://{}/{}/{}/{}?type=f".format(host_1, port_number, function_1, address_2)

tests = [url_1, url_2]

def get_test(key:str):
    res = client.Get(key)
    print("{} -> '{}'".format(key, res))

def get_multiple_test(keys:list[str]):
    res = client.GetMultiple(keys)
    for r in res:
        print("{} -> '{}'".format(r.Key, r.Value))

# TODO compile a regex with named matches to extract the parameters needed by 
# py-modbus to get the actual value.
# probably something like
# modbus_regex = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<func>[a-zA-Z-_.,]+)?/(?P<address>[0-9]+)\?type=?P<type>[fH]')
modbus_pattern = r"^modbus://(?P<host>[a-zA-Z0-9.-]+)/(?P<port>[0-9]+)/(?P<function>[a-zA-Z-_]+)/(?P<address>[0-9]+)\?type=(?P<type>[a-zA-Z]+)$"
if __name__ == "__main__":
    # test the parser
    params = MODbusParams(url_1)
    params.PrintParams()

    assert URL_1 == url_1

    # test Get()
    for t in tests:
        get_test(t)

    # test GetMultiple()
    get_multiple_test([url_1,url_2])