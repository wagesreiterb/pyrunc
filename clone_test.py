#!/usr/bin/python
import sys
from ctypes import *
import time
import subprocess


MIN_PYTHON = (3, 0)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


# https://stackoverflow.com/questions/13373629/clone-process-support-in-python/13374670
# https://stackoverflow.com/questions/37032203/make-syscall-in-python

libc = CDLL("libc.so.6")
mylibc = CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")

# Create stack.
#stack = c_char_p(" " * 8096)    # works in python Python 2.7.15rc1 but not in Python 3.6.7

aaa = " "
stack = c_char_p(aaa.encode('utf-8') * 1024 * 1024)


def f():
    #mylibc.void_and_char_pointer("hallo")

    print(libc.getpid())
    print("hallo")

    time.sleep(1)
    file_child = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "a")
    file_child.write("child\n")
    file_child.close()


    # libc.execve("/bin/sh", 0, 0)
    # subprocess.call("/home/que/PycharmProjects/pyrunc/write_file")

    subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read()
    
    return 0


def call_binary():
    libc.execve("/bin/sh", 0, 0)
    time.sleep(1)

    return 0


# Convert function to c type returning an integer.
f_c = CFUNCTYPE(c_int)(f)
call_binary_c = CFUNCTYPE(c_int)(call_binary)

# We need the top of the stack.
stack_top = c_void_p(cast(stack, c_void_p).value + 8096)

# Call clone with the NEWPID Flag

print("start cloning")
pid = libc.clone(f_c, stack_top, 0x20000000 | 17, 0)        # works
#pid = libc.clone(call_binary_c, stack_top, 0x20000000 | 17, 0)
time.sleep(1)
print(pid)

file = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "a")
file.write("parent\n")
file.close()


# https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
subprocess.call("/bin/sh")