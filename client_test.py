import re

# functions
READ_REGISTER = "read-register"
READ_MULTIPLE_REGISTERS = "read-registers"

# test parameters
host_1 = "192.168.13.3" # change this to the right IP address
function_1 = READ_MULTIPLE_REGISTERS

address_1 = "16386" # voltage
address_2 = "16402" # current
address_3 = "16412" # power 

# read urls for testing
URL_1 = "modbus://192.168.13.3/read-registers/16386?type=f"
url_1 = "modbus://{}/{}/{}?type={}".format(host_1, function_1, address_1, "f")
url_2 = "modbus://{}/{}/{}?type={}".format(host_1, function_1, address_2, "f")
url_3 = "modbus://{}/{}/{}?type={}".format(host_1, function_1, address_3, "f")

tests = [url_1, url_2]

modbus_regex = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<func>[a-zA-Z-_.,]+)?/(?P<address>[0-9]+)\?type=(?P<type>[fH])?')

if __name__ == "__main__":
    # will cause the test to fail if url_1 doesn't match the reference URL_1 
    assert URL_1 == url_1

    for t in tests:
        matches = modbus_regex.match(t)
        
        # groups is a dict that contains a host address, port | None, func,
        # modbus register address, and pymodbus type.
        groups = matches.groupdict()

        # inspect the values encoded in the url
        print(groups)

        # TODO implement a client that sends a GetRequest with a Key of t for each url in tests

    