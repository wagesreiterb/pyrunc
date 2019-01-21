import ctypes
from os import listdir, getcwd
from os.path import isfile, join


libc = ctypes.CDLL("libc.so.6")

# ##############################################################
mypath = "/"
print("-------------------------------------------------------")
print(getcwd())
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
print("-------------------------------------------------------")
# ##############################################################
# chroot
# int chroot(const char *path);
chroot_path = "/home/que/Bernhard/docker/mycontainer/rootfs"
chroot_path_b = chroot_path.encode('utf-8')
chroot_path_p = ctypes.c_char_p(chroot_path_b)
libc.chroot(chroot_path_p)
libc.chdir("/")
print(getcwd())
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
# ##############################################################
print("-------------------------------------------------------")