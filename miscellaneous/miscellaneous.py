import sys


# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append("..")


def check_python_version():
    # Python 2.x had problems with ctpyes.clone
    # Todo: only tested with Python 3.6.7 on Ubuntu 18.04
    min_python = (3, 6)
    if sys.version_info < min_python:
        sys.exit("Python %s.%s or later is required.\n" % min_python)

