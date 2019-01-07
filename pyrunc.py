#!/usr/bin/python

from argparse import ArgumentParser
import sys

parser = ArgumentParser()
subparsers = parser.add_subparsers(help='sub command help')

parser_create = subparsers.add_parser('create', help='help for create')
parser_create.add_argument('container-id')
parser_create.add_argument('--bundle')

args = parser.parse_args()

# sys.exit(1)
