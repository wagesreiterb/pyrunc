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
import numpy

check_python_version()


libc = ctypes.CDLL("libc.so.6")
STACK_SIZE = 1024 * 1024  # http://man7.org/linux/man-pages/man2/clone.2.html
stack = ctypes.c_char_p(" ".encode('utf-8') * STACK_SIZE)
# the clone system call needs the top of the stack
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + STACK_SIZE)

exec_cmd = ""


def call_binary():
    """
    function which is called by the clone system call from the clone function
    """
    #cmd = "./tmp/arg_test.sh"
    cmd_b = exec_cmd.encode('utf-8')     # create byte objects from the strings

    ########## old version ##########
    # args = [exec_cmd, "arg01", "arg02", "arg03", "arg04", "arg05"]
    # length_of_list = len(args)
    # length_of_list += 1  # pointer array must be null-terminated, therefore add 1
    # # initialize the ctypes array of pointers
    # b_argv = (ctypes.c_char_p * length_of_list)(cmd_byte)
    # i = -1
    # for pt in b_argv:
    #     arg = args[i].encode('utf-8')
    #     b_argv[i] = arg
    #     i = i + 1
    # b_argv[i] = None
    ########## old version ##########

    # args = [b'arg1', b'arg2', b'arg3']
    args = ["arg1", "arg2", "arg3", "arg3"]
    args_len = len(args)
    args_b = [None] * args_len  # list for null-terminated char array
    i = 0
    for arg in args:
        args_b[i] = arg.encode('utf-8')
        i += 1

    # https://stackoverflow.com/questions/54279037/call-ctypes-execve-with-dynamic-list-of-argumenst
    cargs = (ctypes.c_char_p * (len(args) + 2))(cmd_b, *args_b, None)

    # int execve(const char * filename, char * const argv[], char * const envp[]);
    ret = libc.execve(ctypes.c_char_p(cmd_b), cargs, 0)  # Todo: envp

    return ret  # Todo: ret only in case of an error -> should be changed to assert


def get_namespaces_flags(list_of_flags):
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

    for flag in list_of_flags:
        print(flag)
        assert (flag in available_flags), "CLONE flag is not available in available_flags"
        flags |= available_flags.get(flag)

    return flags


# Todo: set flags
def clone(cmd, namespaces_list):
    """
    wrapper for the clone system call

    :param cmd: the command which shall be executed
    # Todo: shall be a list of commands taken from "args" in config.json of the container bundle
    """
    global exec_cmd
    exec_cmd = cmd
    assert (exec_cmd != ""), "cmd to be executed is empty"


    call_binary_c = ctypes.CFUNCTYPE(ctypes.c_int)(call_binary)  # convert the function call_binary into C-style

    # pid = libc.clone(call_binary_c, stack_top,
    #                  CLONE_NEWPID | SIGCHLD | CLONE_VFORK | CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWCGROUP | CLONE_NEWNET | CLONE_NEWUSER | CLONE_NEWIPC,
    #                  0)

    # flags_list = ["pid", "network", "ipc", "uts", "mount", "user", "cgroup"]
    namespaces_flags = get_namespaces_flags(namespaces_list)
    # Todo: ^C doesn't work
    pid = libc.clone(call_binary_c, stack_top,
                     namespaces_flags | SIGCHLD | CLONE_VFORK,
                     0)  # Todo: what is that for?!

    assert (pid != -1), "couldn't clone - do you have root permissions?"

    libc.waitpid(pid, None, 0)  # Todo: waitpid shall has its own wrapper most probably
