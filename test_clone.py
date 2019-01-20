#!/usr/bin/python3

from ctypes_wrapper import clone
import sys

# python3 test_clone.py './helloWorld'
# python3 test_clone.py '/bin/sh'

# clone.clone("")
# print(sys.argv[1])
clone.clone(sys.argv[1])
# clone.clone(sys.argv[1])
# clone.clone("/bin/sh")
