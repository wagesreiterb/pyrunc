import ctypes
from miscellaneous.miscellaneous import *

check_python_version()
libc = ctypes.CDLL("libc.so.6")


def waitpid(pid, options):
    # Todo: not fully implemented - only what is needed
    # pid_t waitpid(pid_t pid, int * wstatus, int options);
    # http://man7.org/linux/man-pages/man2/wait.2.html
    libc.waitpid(pid, None, 0)  # Todo: shall this has its own wrapper?!

    # WNOHANG  # return immediately if no child has exited.
    # WUNTRACED  # return if a child has stopped (but not traced via ptrace(2)).Status for traced children which have
                # stopped is provided even if this option is not specified.
    # WCONTINUED  # (since Linux 2.6.10) also return if a stopped child has been resumed by delivery of SIGCONT.

    # options
    # need to be converted from a python list to a flag
    available_options = ["WNOHANG", "WUNTRACED", "WCONTINUED"]

    wstatus = None

    return pid, wstatus
