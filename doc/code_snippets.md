
# **unshare & execvp**
##### works for CLONE_NEWUSER but not for CLONE_NEWPID
```
libc.unshare(CLONE_NEWPID | CLONE_NEWUSER)
cmd = "/bin/sh"
b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)
```
------
##### print PID of process
```
ps aux | grep clone_test.py | grep -v grep | awk '{ print $2 }'
```
------
