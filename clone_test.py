#!/usr/bin/python3

import sys
import ctypes
import time
import subprocess
from signals_flags import *


MIN_PYTHON = (3, 0)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


# https://stackoverflow.com/questions/13373629/clone-process-support-in-python/13374670
# https://stackoverflow.com/questions/37032203/make-syscall-in-python

libc = ctypes.CDLL("libc.so.6")
mylibc = ctypes.CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")

# Create stack.
# stack = c_char_p(" " * 8096)    # works in python Python 2.7.15rc1 but not in Python 3.6.7

STACK_SIZE = 1024 * 1024  # http://man7.org/linux/man-pages/man2/clone.2.html
stack = ctypes.c_char_p(" ".encode('utf-8') * STACK_SIZE)


def f():
    print("entering child function")

    file_child = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "a")
    file_child.write("child\n")
    file_child.close()
    time.sleep(0)

    print("leaving child function")

    # subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read()
    
    return 0


def call_binary():
    print("entering child function")

    # libc.execve("/bin/sh", 0, 0)
    #libc.execvp("/bin/sh", 0, 0)
    #time.sleep(0)

    cmd = "/bin/sh"
    b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
    ret = libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)
    print("call_binary::ret: ", ret)

    print("leaving child function")

    return 0


# Convert function to c type returning an integer.
f_c = ctypes.CFUNCTYPE(ctypes.c_int)(f)
call_binary_c = ctypes.CFUNCTYPE(ctypes.c_int)(call_binary)

# We need the top of the stack.
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + STACK_SIZE)


file = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "a")
file.write("parent\n")
file.close()
time.sleep(0)


# print("start cloning")

pid = libc.clone(call_binary_c, stack_top, CLONE_NEWPID | SIGCHLD | CLONE_VFORK, 0)  # works
# pid = libc.clone(f_c, stack_top, CLONE_NEWPID | SIGCHLD, 0)  # works
print("PID of cloned process: ", pid)
libc.waitpid(pid, None, 0)
# pid = libc.clone(call_binary_c, stack_top, 0x20000000 | 17, 0)


time.sleep(0)



# https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
# subprocess.call("/bin/sh")