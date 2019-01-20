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


check_python_version()


libc = ctypes.CDLL("libc.so.6")
STACK_SIZE = 1024 * 1024  # http://man7.org/linux/man-pages/man2/clone.2.html
stack = ctypes.c_char_p(" ".encode('utf-8') * STACK_SIZE)
# the clone system call needs the top of the stack
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + STACK_SIZE)

exec_cmd = ""


def call_binary():
    # cmd = "/bin/sh"
    cmd_list = ["arg_test.sh", "arg_1", "arg_2"]
    b_cmd = exec_cmd.encode('utf-8')     # create byte objects from the strings

    argv_1 = "argv_1"
    b_argv_1 = argv_1.encode('utf-8')

    argv = (ctypes.c_char_p * 2)(b_cmd)

    env0_string = "USER=root"
    env0 = env0_string.encode('utf-8')
    envp = (ctypes.c_char_p * 2)(env0)

    # int execve(const char * filename, char * const argv[], char * const envp[]);
    ret = libc.execve(ctypes.c_char_p(b_cmd), argv, envp)

    return ret


# Todo: set flags
def clone(cmd):
    global exec_cmd
    exec_cmd = cmd
    assert (exec_cmd != ""), "cmd to be executed is empty"

    # convert the function call_binary into C-style
    call_binary_c = ctypes.CFUNCTYPE(ctypes.c_int)(call_binary)
    pid = libc.clone(call_binary_c, stack_top,
                     CLONE_NEWPID | SIGCHLD | CLONE_VFORK | CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWCGROUP | CLONE_NEWNET | CLONE_NEWUSER | CLONE_NEWIPC,
                     0)

    assert (pid != -1), "couldn't clone - do you have root permissions?"

    libc.waitpid(pid, None, 0)  # Todo: waitpid shall have its own wrapper most probably
