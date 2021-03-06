#################################################################################
#                                                                               #
# if we call a python function, then the parent group within the child          #
# isn't set correctly?!                                                         #
# getpgrp():  0                                                                 #
#                                                                               #
#################################################################################


import ctypes
from signals_flags import *
from miscellaneous.miscellaneous import *
from ctypes_wrapper.sethostname import *
from ctypes_wrapper.chroot import *
from ctypes_wrapper.waitpid import *


check_python_version()

libc = ctypes.CDLL("libc.so.6")
STACK_SIZE = 1024 * 1024  # http://man7.org/linux/man-pages/man2/clone.2.html
stack = ctypes.c_char_p(" ".encode('utf-8') * STACK_SIZE)
# the clone system call needs the top of the stack
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + STACK_SIZE)

exec_cmd = ""
exec_args = ""


def call_binary():
    """
    function which is called by the clone system call from the clone function
    """
    chroot("/home/que/Bernhard/docker/busybox/rootfs", "/")
    set_hostname("pyrunc")

    mount()

    #libc.setsid()
    #ret_setuid = libc.setuid(0)




    # cmd = "./tmp/arg_test.sh"
    cmd_b = exec_cmd.encode('utf-8')     # create byte objects from the strings

    # ############### args ###############
    # args = ["arg1", "arg2", "arg3", "arg3"]
    args_len = len(exec_args)
    args_b = [None] * args_len  # list for null-terminated char array
    i = 0
    for arg in exec_args:
        args_b[i] = arg.encode('utf-8')
        i += 1
    # https://stackoverflow.com/questions/54279037/call-ctypes-execve-with-dynamic-list-of-argumenst
    cargs = (ctypes.c_char_p * (len(exec_args) + 2))(cmd_b, *args_b, None)
    # ############### args ###############

    # ############### env ###############
    env_dict = {
        "SHLVL": "1",
        "LANGUAGE": "en_US"
    }

    env_list = ["SHLVL=1", "LANGUAGE=en_US"]

    env_list_len = len(env_list)
    env_b = [None] * env_list_len  # list for null-terminated char array
    i = 0
    for entry in env_list:
        env_b[i] = entry.encode('utf-8')
        i += 1
    # https://stackoverflow.com/questions/54279037/call-ctypes-execve-with-dynamic-list-of-argumenst
    env_p = (ctypes.c_char_p * (len(env_list) + 2))(*env_b, None)
    # ############### env ###############

    # int execve(const char * filename, char * const argv[], char * const envp[]);
    # ret = libc.execve(ctypes.c_char_p(cmd_b), cargs, 0)  # Todo: envp
    ret = libc.execve(ctypes.c_char_p(cmd_b), cargs, env_p)

    return ret  # Todo: ret only in case of an error -> should be changed to assert


def get_namespaces_flags(namespaces_list):
    """
    converts a list of namespaces into a flag
    :param command: the command which shall executed within the container
        ["pid", "network", "ipc", "uts", "mount", "user", "cgroup"]
    :returns the flag for the namespaces
    """
    # https://github.com/opencontainers/runtime-spec/blob/master/config.md
    available_flags = {
        "pid": CLONE_NEWPID,
        "network": CLONE_NEWNET,
        "ipc": CLONE_NEWIPC,
        "uts": CLONE_NEWUTS,
        "mount": CLONE_NEWNS,
        "user": CLONE_NEWUSER,
        "cgroup": CLONE_NEWCGROUP
    }

    flags = 0x00

    for flag in namespaces_list:
        assert (flag in available_flags), "CLONE flag is not available in available_flags"
        flags |= available_flags.get(flag)

    return flags


def clone(command, namespaces_list, args_list):
    """
    wrapper for the clone system call
    :param command: the command which shall executed within the container
        "/bin/sh"
    :param namespaces_list: list of namespaces for the container
        ["pid", "network", "ipc", "uts", "mount", "user", "cgroup"]
    :param args_list: list of arguments passed to the called command
    # Todo: shall be a list of commands taken from "args" in config.json of the container bundle
    """

    # Todo: it should be possible to pass arguments to call_binary - just didn't figure out how
    global exec_cmd
    exec_cmd = command
    global exec_args
    exec_args = args_list
    assert (exec_cmd != ""), "command to be executed is empty"

    call_binary_c = ctypes.CFUNCTYPE(ctypes.c_int)(call_binary)  # convert the function call_binary into C-style

    namespaces_flags = get_namespaces_flags(namespaces_list)
    # Todo: ^C doesn't work
    # Todo: after exiting a "sh" the following error is print "/bin/sh: 11: Cannot set tty process group (No such process)"

    # int clone(int(*fn)(void *), void * child_stack, int flags, void * arg, ...
    # / * pid_t * ptid, void * newtls, pid_t * ctid * / );
    pid = libc.clone(call_binary_c, stack_top,
                     namespaces_flags | SIGCHLD | CLONE_VFORK,
                     0)  # Todo: what is that for?!

    assert (pid != -1), "couldn't clone - do you have root permissions?"

    child_pid = waitpid(pid, 0)


def mount():
    ########## mount ##########
    # http://advinpy.blogspot.com/2015/11/mount-and-umount-with-ctypes.html
    #mountSource = "/home/addy/workspace/pymount/test3".encode(encoding='ascii', errors='replace')
    #mountTarget = "/home/addy/workspace/pymount/test4".encode(encoding='ascii', errors='replace')
    #retCode = libc.mount(mountSource, mountTarget, None, 4096, None)

    #int mount(const char * source,
    #            const char * target,
    #            const char * filesystemtype,
    #            unsigned long mountflags,
    #            const void * data
    #        );
    mountSource = "proc".encode(encoding='ascii', errors='replace')
    mountTarget = "/proc".encode(encoding='ascii', errors='replace')
    fsType = "proc".encode(encoding='ascii', errors='replace')
    libc.mount(mountSource, mountTarget, fsType, None, None)


    mountSource = "sysfs".encode(encoding='ascii', errors='replace')
    mountTarget = "/sys".encode(encoding='ascii', errors='replace')
    fsType = "sysfs".encode(encoding='ascii', errors='replace')
    flags = "ro".encode(encoding='ascii', errors='replace')

    # https://elixir.bootlin.com/linux/v4.3/source/include/uapi/linux/fs.h  # L68
    MS_RDONLY = 1  # Mount read-only
    libc.mount(mountSource, mountTarget, fsType, MS_RDONLY, None)

    ########## mount ##########





