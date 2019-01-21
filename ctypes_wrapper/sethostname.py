from ctypes import *
from constants import *


libc = CDLL("libc.so.6")


def set_hostname(hostname):
    # int sethostname(const char * name, size_t len);

    assert (len(hostname) <= MAX_HOSTNAME_LENGTH), "the length of the hostname is > " + str(MAX_HOSTNAME_LENGTH)

    # Todo: check for not allowed characters in the hostname

    hostname_p = c_char_p(hostname.encode('utf-8'))
    libc.sethostname(hostname_p, len(hostname))
