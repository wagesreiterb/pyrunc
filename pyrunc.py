#!/usr/bin/python

from argparse import ArgumentParser
import sys

parser = ArgumentParser(prog='pyrunc.py')
subparsers = parser.add_subparsers(help='sub command help')
parser_create = subparsers.add_parser('create', help='help for create')
parser_create.add_argument('container-id')
parser_create.add_argument('--bundle')

parser.add_argument('--debug', help='enable debug output for logging', action='store_true')
parser.add_argument('--log', help='set the log file path where internal debug information is written', default='/dev/null')
parser.add_argument('--log-format', help="set the format used by logs ('text' (default), or 'json')", default='text')
parser.add_argument('--root', help='root directory for storage of container state (this should be located in tmpfs)', default='root')
parser.add_argument('--criu', help='path to the criu binary used for checkpoint and restore', default='criu')
parser.add_argument('--systemd-cgroup', help='enable systemd cgroup support, expects cgroupsPath to be of form "slice:prefix:name" for e.g. "system.slice:runc:434234"', action='store_false')
parser.add_argument('--rootless', help="ignore cgroup permission errors ('true', 'false', or 'auto')", default='auto')
parser.add_argument('--version', help='print the version', action='store_true')


args = parser.parse_args()

if args.version:
   print("pyrunc version 0.1.0")
   print("spec: 1.0")
