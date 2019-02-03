from libcontainer.mount import *


class Config:
    def __init__(self):
        self.no_pivot_root = False
        self.rootfs = ''
        self.mounts = Mount()
        '''
        self.mounts = [
                            {
                                "source": "proc",
                                "destination": "/proc",
                                "device": "proc",
                                "flags": 0,
                                "propagation_flags": None,
                                "data": "",
                                "relabel": "",
                                "extensions": 0,
                                "premount_cmds": None,
                                "postmount_cmds": None
                            }
                        ]
        '''

    def serializer(self):
        print("Config serializer")
        serial = dict()
        serial['no_pivot_root'] = self.no_pivot_root
        serial['rootfs'] = self.rootfs
        serial["mounts"] = self.mounts.serializer()
        return serial

    def deserializer(self, json_data):
        print("Config deserializer")
        if 'no_pivot_root' in json_data:
            self.no_pivot_root = json_data["no_pivot_root"]
        if 'rootfs' in json_data:
            self.rootfs = json_data["rootfs"]
        if 'mounts' in json_data:
            self.mounts = json_data["mounts"]
