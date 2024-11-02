import re

# functions
READ_REGISTER = "read-register"
READ_MULTIPLE_REGISTERS = "read-registers"

# test parameters
host_1 = "192.168.13.3" # change this to the right IP address
function_1 = READ_MULTIPLE_REGISTERS

address_1 = "16386" # voltage
address_2 = "16402" # current

# read urls for testing
URL_1 = "modbus://{}"
url_1 = "modbus://{}/{}/{}?type={}".format(host_1, function_1, address_1)
url_2 = "modbus://{}/{}/{}?type={}".format(host_1, function_1)

tests = [url_1, url_2]

# TODO compile a regex with named matches to extract the parameters needed by 
# py-modbus to get the actual value.
# probably something like
# modbus_regex = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<func>[a-zA-Z-_.,]+)?/(?P<address>[0-9]+)\?type=?P<type>[fH]')


if __name__ == "__main__":
    assert URL_1 == url_1

    for t in tests:
        # TODO write a client that sends a GetRequest with a Key of t for each url in tests
        pass