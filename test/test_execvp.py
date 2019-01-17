#!/usr/bin/python3

# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure/24266885#24266885

from ctypeswrapper import execvp
import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_execvp_version(self):
        self.assertEqual(execvp.print_version(), 'Version 1.0')

    def test_execvp_execvp(self):
        #ret = execvp.execvp("/bin/sh -c 'echo hallo'")
        ret = execvp.execvp("/bin/sh")
        print("xxx")
        print("ret", ret)
        print("xxx")
        self.assertEqual(execvp.print_version(), 'Version 1.0')

    def test_lstrip(self):  # testing for left stripping
        self.assertEqual('   hello '.lstrip(), 'hello ')

    def test_isupper(self):  # testing for isupper
        self.assertTrue('HELLO'.isupper())
        self.assertFalse('HELlO'.isupper())

    def test_split(self):  # testing for split
        self.assertEqual('Hello World'.split(), ['Hello', 'World'])
        with self.assertRaises(TypeError):
            'Hello World'.split(2)


if __name__ == '__main__':
    unittest.main()
