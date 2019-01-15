import ctypes
import os


# https://stackoverflow.com/questions/5081875/ctypes-beginner

# gcc -shared -Wl,-soname,testlib -o testlib.so -fPIC testlib.c
os.system("gcc -shared -Wl,-soname,testlib -o testlib.so -fPIC testlib.c")


libc = ctypes.CDLL("libc.so.6")


mylibc = ctypes.CDLL("/home/que/PycharmProjects/pyrunc/testlib.so")


# void void_and_void()
mylibc.void_and_void()

# int int_and_void()
print("int_and_void(): ", mylibc.int_and_void())

#int void_and_int(int arg)
mylibc.void_and_int(13)

#void_and_char_pointer
mylibc.void_and_char_pointer("hallo")

mylibc.void_and_void_pointer("abcd")

mylibc.sleeper(60)
