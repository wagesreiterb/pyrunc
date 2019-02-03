# https://github.com/opencontainers/runc/blob/master/libcontainer/configs/mount.go
class Mount:
    def __init__(self):
        self.source = ""
        self.destination = ""
        self.flags = 0x00

    #def __init__(self):
    #    _fields = [('source', str), ('destination', str), ('flags', int)]

    def serializer(self):
        print("Mount serializer")
        serial = dict()
        serial['source'] = self.source
        serial['destination'] = self.destination
        serial['flags'] = self.flags
        return serial

    def deserializer(self, json_data):
        print("Mount deserializer")
        if 'source' in json_data:
            self.source = json_data["source"]
        if 'destination' in json_data:
            self.destination = json_data["destination"]
        if 'flags' in json_data:
            self.flags = json_data["flags"]
