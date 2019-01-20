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
    cmd_byte = exec_cmd.encode('utf-8')     # create byte objects from the strings

    '''
    ### works ### ### works ### ### works ### ### works ###

    argv_0 = "argv_0"
    argv_0_byte = argv_0.encode('utf-8')

    argv_1 = "argv_1"
    argv_1_byte = argv_1.encode('utf-8')

    argv_2 = "argv_2"
    argv_2_byte = argv_2.encode('utf-8')

    argv_3 = "argv_3"
    argv_3_byte = argv_3.encode('utf-8')

    b_argv = (ctypes.c_char_p * 5)(argv_0_byte, argv_1_byte, argv_2_byte, argv_3_byte)

    ### works ### ### works ### ### works ### ### works ###
    '''

    b_argv = (ctypes.c_char_p * 5)(cmd_byte)
    # int execve(const char * filename, char * const argv[], char * const envp[]);
    ret = libc.execve(ctypes.c_char_p(cmd_byte), b_argv, 0)

    return ret


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
    pid = libc.clone(call_binary_c, stack_top,
                     namespaces_flags | SIGCHLD | CLONE_VFORK,
                     0)  # Todo: what is that for?!

    assert (pid != -1), "couldn't clone - do you have root permissions?"

    libc.waitpid(pid, None, 0)  # Todo: waitpid shall have its own wrapper most probably



#######################################################################################

    #hello = b"Hello World"
    #ctypes.c_char_p(argv_1_byte)

    # a = (ctypes.c_void_p * 2)

    #for i in range(4):
    #    argv = "argv"
    #    argv_byte = argv.encode('utf-8')
    #    ctypes.c_char_p(argv_byte)

    #string_buffers = ((ctypes.c_char * 6) * 4)()
    #string_buffers[1] = ctypes.create_string_buffer(b"Hello")

    #p = ctypes.create_string_buffer(b"Hello")  # create a buffer containing a NUL terminated string
    #my_array = ctypes.c_char_p * 10

    # string_buffers[1] = argv_1
    #argv_1 = "argv_1"
    #argv_1_byte = argv_1.encode('utf-8')

    #xxx = (ctypes.c_char_p * 10)(8)
    #pi = ctypes.pointer(xxx)
    #string_buffer = ctypes.create_string_buffer(b"Hello", 10)
    #string_buffer_p = ctypes.pointer(ctypes.cast(string_buffer, ctypes.c_char_p))
    #pi[0] = string_buffer_p


    # argv_list = ["./tmp/arg_test.sh", "arg_1", "arg_2"]
    # for arg in argv_list:
    #    print(arg)




    #a = numpy.array(['apples', 'foobar', 'cowboy'])
    #a[2] = 'bananas'
    #print(a)
    #a.ctypes.data_as(ctypes.POINTER(ctypes.c_char)).contents



    #env0_string = "USER=root"
    #env0 = env0_string.encode('utf-8')
    #envp = (ctypes.c_char_p * 2)(env0)