# parse the url
import re

modbus_pattern = r"^modbus://(?P<host>[a-zA-Z0-9.-]+)/(?P<port>[0-9]+)/(?P<function>[a-zA-Z-_]+)/(?P<address>[0-9]+)\?type=(?P<type>[a-zA-Z]+)$"
class MODbusParams():
    def __init__(self, url) -> None:
        match = re.match(modbus_pattern, url)
        # Extract components if the pattern matches
        if match:
            self.host = match.group("host")
            self.port = match.group("port")
            self.function = match.group("function")
            self.address = match.group("address")
            self.type_param = match.group("type")

        else:
            print("URL does not match the expected format.")
            self.host = ""
            self.port = ""
            self.function = ""
            self.address = ""
            self.type_param = ""

    def PrintParams(self):
        # Print extracted values
        print("Host:", self.host)
        print("Port:", self.port)
        print("Function:", self.function)
        print("Address:", self.address)
        print("Type:", self.type_param)
    
