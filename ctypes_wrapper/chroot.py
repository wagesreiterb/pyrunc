from ctypes import *


libc = CDLL("libc.so.6")


def chroot(rootfs_path, cwd):
    # Todo: cwd shall be optional, if it is missing then CWD = "/"
    chroot_path_p = c_char_p(rootfs_path.encode('utf-8'))
    ret = libc.chroot(chroot_path_p)
    assert (ret != -1), "couldn't chroot into directory " + rootfs_path

    chdir_path = cwd  # "/"
    chdir_path_p = c_char_p(chdir_path.encode('utf-8'))
    libc.chdir(chdir_path_p)



    #chroot_path = "/home/que/Bernhard/docker/ubuntu/rootfs"
    #chroot_path_b = chroot_path.encode('utf-8')
    #chroot_path_p = ctypes.c_char_p(chroot_path_b)
    #libc.chroot(chroot_path_p)

    #chdir_path = "/"
    #chdir_path_b = chdir_path.encode('utf-8')
    #chdir_path_p = ctypes.c_char_p(chdir_path_b)
    #libc.chdir(chdir_path_p)