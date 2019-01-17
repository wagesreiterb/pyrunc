#!/usr/bin/python

import ctypes
import sys


# Python 2.x had problems with ctpyes.clone
MIN_PYTHON = (3, 0)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

libc = ctypes.CDLL("libc.so.6")


def execvp(cmd):
    # cmd = "/bin/sh"
    b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
    libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)


def print_version():
    return "Version 1.0"
