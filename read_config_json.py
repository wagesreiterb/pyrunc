import json
import os


# https://docs.python.org/3/library/json.html
#
# Python 	                                JSON
# ------------------------------------------------
# dict                                      object
# list, tuple 	                            array
# str                                       string
# int, float, int- & float-derived Enums 	number
# True 	                                    true
# False 	                                false
# None 	                                    null


with open("config.json") as datafile:
    data = json.load(datafile)

#print(data)


ociVersion = data["ociVersion"]


# process
print("process:args", data["process"]["args"])

# root
print("----------------------------------------")
print("##### root #####")
print("root:path", data["root"]["path"])
print("root:readonly", data["root"]["readonly"])


# hostname
print("----------------------------------------")
print("##### hostname #####")
print("hostname:", data["hostname"])


# mounts


# linux
print("----------------------------------------")
print("##### linux #####")
for namespace in data["linux"]["namespaces"]:
    print(namespace)


# start process within container
# unshare --fork --pid --ipc --mount --net --uts /bin/bash
cmd_unshare = "unshare"
attr_fork = " --fork"
attr_pid = " --pid" + " --mount-proc"
attr_ipc = " --ipc"
attr_mount = " --mount"
attr_net = " --net"
attr_uts = " --uts" + "=" + "/home/que/Bernhard/docker/mycontainer/rootfs/etc/hostname"

cmd = cmd_unshare \
        + attr_fork \
        + attr_pid \
        + attr_ipc \
        + attr_mount \
        + attr_net \
        + attr_uts

print("cmd: ", cmd)

returned_value = os.system(cmd)  # returns the exit code in unix
print('returned value:', returned_value)
