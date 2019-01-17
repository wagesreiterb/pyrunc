import subprocess
import os
import ctypes


libc = ctypes.CDLL("libc.so.6")


subprocess.run(["/usr/bin/sum", "/bin/sh"])

path_to_chroot = "/home/que/Bernhard/docker/mycontainer"
#ret = os.chroot(path_to_chroot)
#print("ret chroot: ", ret)
#ret = os.chdir('/')
#print("ret chdir: ", ret)


path_to_chroot = "/home/que/Bernhard/docker/mycontainer"
ret = libc.chroot(path_to_chroot)
print("ret chroot: ", ret)
subprocess.run(["pwd"])


ret = libc.chdir("/home/que/Bernhard/docker/mycontainer/rootfs/")
print("ret chdir: ", ret)
subprocess.run(["pwd"])
# subprocess.run(["/usr/bin/sum", "/bin/sh"])
# subprocess.run(["env"])



# subprocess.run(["sum", "/home/que/Bernhard/docker/mycontainer/rootfs/bin/sh"])
