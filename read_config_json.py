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
process_args = str(data["process"]["args"][0])  # Todo: there can be more than one arg

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
cmd_unshare = "unshare "
attr_fork = "--fork "
attr_pid = "--pid" + " --mount-proc "
attr_ipc = "--ipc "
attr_mount = "--mount "
attr_net = "--net "
attr_uts = "--uts" + "=" + "/home/que/Bernhard/docker/mycontainer/rootfs/etc/hostname "

cmd = cmd_unshare \
        + attr_fork \
        + attr_pid \
        + attr_ipc \
        + attr_mount \
        + attr_net \
        + attr_uts


container_hostname = "pyrunc"
container_rootfs = "/home/que/Bernhard/docker/mycontainer/rootfs"

cmd_exec = "sh -c '"

#cmd_exec += '/bin/hostname ' + container_hostname + "; "    # sets the hostname
#cmd_exec += 'PS1=> ;'

# cmd_exec += '''for i in $(env | awk -F"=" '{print $1}') ; do unset $i ; done'''
# cmd_exec += "unset $(env |awk -F'=' '{print $1}'); "
#cmd_exec += '''env | awk -F"=" '{print $1}'; '''
cmd_exec += 'env; echo "xxxxxxxxxxxxxxxxxxxxxxxxxxx"'
cmd_exec += 'for i in `env | sed "s/ //g"`; do k=`echo $i | cut -d "=" -f 1`; unset "$k"; done; '
# for i in `env | sed 's/ //g'`; do echo $i; k=`echo $i | cut -d "=" -f 1`; echo "$k"; echo; done
cmd_exec += 'env; echo "yyyyyyyyyyyyyyyyyyyyyyyyyyy"'
cmd_exec += 'env; '
#cmd_exec += 'chroot ' + container_rootfs + " "              # sets the new root directory to the one within the OCI bundle
#cmd_exec += process_args        # sh
cmd_exec += "'"

cmd = cmd + cmd_exec

print("cmd: ", cmd)
print("")
print("")

returned_value = os.system(cmd)  # returns the exit code in unix

print("")
print("")
print('returned value:', returned_value)
