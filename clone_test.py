from ctypes import *
import time

# https://stackoverflow.com/questions/13373629/clone-process-support-in-python/13374670
# https://stackoverflow.com/questions/37032203/make-syscall-in-python

libc = CDLL("libc.so.6")
mylibc = CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")

# Create stack.
stack = c_char_p(" " * 8096)


def f():
    mylibc.void_and_char_pointer("hallo")
    print(libc.getpid())
    print("hallo")

    file = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "w")
    file.write("child")
    file.close()

    time.sleep(5)
    
    return 0


# Convert function to c type returning an integer.
f_c = CFUNCTYPE(c_int)(f)

# We need the top of the stack.
stack_top = c_void_p(cast(stack, c_void_p).value + 8096)

# Call clone with the NEWPID Flag
pid = libc.clone(f_c, stack_top, 0x20000000 | 17, 0)
time.sleep(10)
print(pid)

file = open("/home/que/PycharmProjects/pyrunc/testfile.txt", "w")
file.write("parent")
file.close()



# (56, signal.SIGCHLD|0x000200000, 0)
# print(libc.syscall(39))
