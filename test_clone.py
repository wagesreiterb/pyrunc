#!/usr/bin/python3

from ctypes_wrapper import clone
import sys

# python3 test_clone.py './helloWorld'
# python3 test_clone.py '/bin/sh'

# clone.clone("")
# print(sys.argv[1])

flags_list = ["pid", "network", "ipc", "uts", "mount", "user", "cgroup"]
args_list = []
clone.clone(sys.argv[1], flags_list, args_list)



# clone.clone(sys.argv[1])
# clone.clone("/bin/sh")
