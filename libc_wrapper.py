import ctypes
import time

# https://stackoverflow.com/questions/13373629/clone-process-support-in-python/13374670

def myfunc():
    #libc.execve("/bin/sh", "", "")
    mylibc.sleeper()


libc = ctypes.CDLL("libc.so.6")
mylibc = ctypes.CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")


STACK_SIZE = 1024 * 1024
#child_stack = bytearray(STACK_SIZE)
child_stack = ctypes.c_char * STACK_SIZE
child_stack_instance = child_stack()
#child_stack_instance_byref = ctypes.byref(child_stack_instance) + STACK_SIZE
child_stack_instance_pointer = ctypes.cast(child_stack_instance, ctypes.POINTER(ctypes.c_char)).contents

#print("child_stack_instance type:", type(child_stack_instance))
#print("child_stack_instance:", child_stack_instance)
#print("child_stack_instance_byref:", child_stack_instance_byref)




#child_pid = libc.clone(myfunc, child_stack_instance_pointer, 0x07)


# define CLONE_NEWPID	0x20000000	/* New pid namespace */
# define CLONE_NEWUSER	0x10000000	/* New user namespace */
# define CLONE_VM	0x00000100	/* set if VM shared between processes */
# https://github.com/torvalds/linux/blob/master/include/uapi/linux/sched.h

child_pid = libc.clone(mylibc.sleeper(10), child_stack_instance, 0x20000000 | 17 | 0x00000100, 0)    # Todo: child_stack_instance + STACK_SIZE
print(child_pid)
time.sleep(10)

#mylibc.sleeper(60)

#print(child_pid)

#child_pid = libc.clone(myfunc, bled, 0x07)









