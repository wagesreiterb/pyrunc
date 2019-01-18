#!/usr/bin/python3

# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure/24266885#24266885

from ctypes_wrapper import execvp
import unittest


class TestExecvp(unittest.TestCase):
    def setUp(self):
        pass

    def test_execvp_execvp(self):
        ret = execvp.execvp("/bin/sh")
        self.assertEqual(ret, 0)


if __name__ == '__main__':
    unittest.main()


# # python3 -m unittest test.test_execvp
# $ exit
