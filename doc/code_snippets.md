
# **unshare & execvp**
##### works for CLONE_NEWUSER but not for CLONE_NEWPID
```
libc.unshare(CLONE_NEWPID | CLONE_NEWUSER)
cmd = "/bin/sh"
b_cmd = cmd.encode('utf-8')     # create byte objects from the strings
libc.execvp(ctypes.c_char_p(b_cmd), 0, 0)
```
------
##### print all files of the directory
```
mypath = "/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
```
------
##### print PID of process
```
ps aux | grep clone_test.py | grep -v grep | awk '{ print $2 }'
```
------
https://github.com/opencontainers/runc
```
docker export $(docker create ubuntu) | tar -C rootfs -xvf -
runc spec
```
------