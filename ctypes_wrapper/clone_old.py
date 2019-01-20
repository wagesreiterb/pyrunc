import ctypes
from signals_flags import *
from miscellaneous.miscellaneous import *


check_python_version()


# Todo: set flags
def clone(cmd):
    assert (cmd != ""), "cmd to be executed is empty"

    # Todo: doesn't clone at all o-)
    pid = libc.clone(libc.execvp(ctypes.c_char_p(cmd.encode('utf-8')), 0, 0),
                     stack_top,
                     CLONE_NEWPID | SIGCHLD | CLONE_VFORK | CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWCGROUP | CLONE_NEWNET | CLONE_NEWUSER | CLONE_NEWIPC,
                     0)
    print("pid: ", pid)
    assert (pid != -1), "couldn't clone - do you have root permissions?"

    libc.waitpid(pid, None, 0)  # Todo: waitpid shall have its own wrapper most probably


libc = ctypes.CDLL("libc.so.6")
STACK_SIZE = 1024 * 1024  # http://man7.org/linux/man-pages/man2/clone.2.html
stack = ctypes.c_char_p(" ".encode('utf-8') * STACK_SIZE)
# the clone system call needs the top of the stack
stack_top = ctypes.c_void_p(ctypes.cast(stack, ctypes.c_void_p).value + STACK_SIZE)
