from libcontainer.config import *


class BaseState:
    def __init__(self):
        self.id = ""
        self.init_process_pid = 0
        self.init_process_start = 0
        self.created = 0
        self.config = Config()
        # self.id = ""
        #self.runtime_status = RuntimeStates.Stopped   # initial state of the container

    def serializer(self):
        print("BaseState serializer")
        serial = dict()
        serial["id"] = self.id
        serial["init_process_pid"] = self.init_process_pid
        serial["init_process_start"] = self.init_process_start
        serial["created"] = self.created
        serial["config"] = self.config.serializer()
        return serial


    def deserializer(self, json_data):
        if 'id' in json_data:
            self.id = json_data["id"]
        if 'init_process_pid' in json_data:
            self.init_process_pid = json_data["init_process_pid"]
        if 'init_process_start' in json_data:
            self.init_process_start = json_data["init_process_start"]
        if 'created' in json_data:
            self.created = json_data["created"]


'''
// BaseState represents the platform agnostic pieces relating to a
// running container's state
type BaseState struct {
	// ID is the container ID.
	ID string `json:"id"`

	// InitProcessPid is the init process id in the parent namespace.
	InitProcessPid int `json:"init_process_pid"`

	// InitProcessStartTime is the init process start time in clock cycles since boot time.
	InitProcessStartTime uint64 `json:"init_process_start"`

	// Created is the unix timestamp for the creation time of the container in UTC
	Created time.Time `json:"created"`

	// Config is the container's configuration.
	Config configs.Config `json:"config"`
}
'''