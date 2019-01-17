#!/usr/bin/python
import sys
import ctypes
import time
import subprocess


MIN_PYTHON = (3, 0)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


# https://stackoverflow.com/questions/13373629/clone-process-support-in-python/13374670
# https://stackoverflow.com/questions/37032203/make-syscall-in-python

libc = ctypes.CDLL("libc.so.6")
mylibc = ctypes.CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")

# Create stack.
#stack = c_char_p(" " * 8096)    # works in python Python 2.7.15rc1 but not in Python 3.6.7

aaa = " "
stack = ctypes.c_char_p(aaa.encode('utf-8') * 1024 * 1024)


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
f_c = ctypes.CFUNCTYPE(ctypes.c_int)(f)
call_binary_c = ctypes.CFUNCTYPE(ctypes.c_int)(call_binary)

# We need the top of the stack.
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + 8096)

# Call clone with the NEWPID Flag
CLONE_NEWPID = 0x20000000   # New pid namespace
CLONE_NEWUSER = 0x10000000  # New user namespace


#print("start cloning")
#pid = libc.clone(f_c, stack_top, 0x20000000 | 17, 0)        # works
#pid = libc.clone(call_binary_c, stack_top, 0x20000000 | 17, 0)


time.sleep(30)

#####################################################################
# works for CLONE_NEWUSER but not for CLONE_NEWPID
libc.unshare(CLONE_NEWPID | CLONE_NEWUSER)
cmd = "/bin/sh"
b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)
#####################################################################



file = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "a")
file.write("parent\n")
file.close()


# https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
#subprocess.call("/bin/sh")