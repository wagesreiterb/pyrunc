import sys
# https://stackoverflow.com/questions/3144089/expand-python-search-path-to-other-source
sys.path.append(".")  # Todo: not sure whether this is the best solution

from enum import Enum
import json
from miscellaneous.miscellaneous import *
from libcontainer.basestate import *
from datetime import datetime

check_python_version()


# https://github.com/opencontainers/runc/blob/master/libcontainer/container.go
class RuntimeStates(Enum):
    Created = 0
    Running = 1
    Pausing = 2
    Paused = 3
    Stopped = 4


class Container:
    def __init__(self):
        self.basestate = BaseState()

    def serializer(self):
        print("Container serializer")
        #serial = self.container
        serial = dict()
        #serial["basestate"] = self.basestate.serializer()
        print(self.basestate.serializer())
        return serial

    def deserializer(self, json_data):
        print("Container deserializer")
        self.basestate = json_data

    @staticmethod
    def get_status_as_string(status):
        status_as_string = "unknown"
        if status == RuntimeStates.Created:
            status_as_string = "created"
        elif status == RuntimeStates.Running:
            status_as_string = "running"
        elif status == RuntimeStates.Pausing:
            status_as_string = "pausing"
        elif status == RuntimeStates.Paused:
            status_as_string = "paused"
        elif status == RuntimeStates.Stopped:
            status_as_string = "stopped"
        return status_as_string

    def json_as_string(self):
        return json.dumps(self, default=serialize)

    def json_as_dict(self):
        as_dict = json.loads(self.json_as_string())
        return as_dict['container']


# https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json/10252138
# https://code-maven.com/serialize-datetime-object-as-json-in-python
def serialize(obj):
    # JSON serializer for objects not serializable by default json code
    #if isinstance(obj, Container):
    #    print("is instace of ", type(obj))
    #    serial = obj.serializer()
    #    return serial
    #else:
    return obj.__dict__


##### test serializer ######
#my_container = BaseState()
#my_container = Container()
#print(json.dumps(my_container.container, default=serialize))
##### test serializer ######



##### test deserializer ######
# test load a containers state.json an deserialize it
#'''
with open("./tmp/test.json") as json_file:
    json_dict = json.load(json_file)
    #print(type(json_dict))
    print(json_dict)

    print("---------------------------------------------------------")
    my_container2 = Container()
    my_container2.deserializer(json_dict)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    my_container2_as_json = json.dumps(my_container2, default=serialize)
    print("#########################################################")
    print(type(my_container2.basestate))
    print(my_container2.basestate['id'])
    print(my_container2.basestate['init_process_pid'])
    print(my_container2.basestate['config'])
    print(my_container2.basestate['config']['no_pivot_root'])
    print(my_container2.basestate['config']['rootfs'])
    print(my_container2.basestate['config']['mounts'])
    print(my_container2.basestate['config']['mounts'][0]['source'])


    print('**********************************************************')
    print("my_container2_as_json")
    my_container2_as_str = json.dumps(my_container2, default=serialize)
    print(type(my_container2_as_json))
    my_container2_as_json = json.loads(my_container2_as_str)
    print(my_container2_as_json['basestate'])

    #print(json.dumps(my_container2, default=serialize))
    #print(type(my_container2_as_json))
    #print("---------------------------------------------------------")
    #my_container2_as_dict = json.loads(my_container2_as_json)
    #print(type(my_container2_as_dict))
    #print(my_container2_as_dict)
    #print(my_container2_as_dict['container'])
    #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(my_container2.json_as_dict())
    #print(type(my_container2))


    #my_container2.container.created = datetime.now()

    #print(my_container2.id)
    #print(my_container2.init_process_pid)
    #print(json.dumps(my_container2.config, default=serialize))
    #print(my_container2.config.mounts[0].source)
#'''
##### test deserializer ######




#dump = json.dumps(my_container, default=serialize)
#serialized_container = my_container.serializer()
#print(serialized_container)

