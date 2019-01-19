#!/usr/bin/python3

import ctypes
from miscellaneous.miscellaneous import *

check_python_version()
libc = ctypes.CDLL("libc.so.6")


def execvp(cmd):
    # cmd = "/bin/sh"
    b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
    ret = libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)
    assert (ret == 0), "libc.execvp couldn't execute file"
