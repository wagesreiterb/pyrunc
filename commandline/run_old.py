
'''

import re


def create_subparser(parser, subparsers):
    subparser_run = subparsers.add_parser('run')

    subparser_run.add_argument('containerID')
    subparser_run.add_argument('--detach', action='store_true', help="detach from the container's process")
    # Todo: the rest of the arguments are missing

    args = parser.parse_args()

    if(args.containerID):
        run_container(args.containerID)
    if(args.detach):
        print("detach argument has been provided")
        # Todo:


    return subparser_run


def run_container(containerid):
    print("run_container")
    # check if the container has a valid format
    is_conatinerid_valid(containerid)

    # Todo: start the container


def is_conatinerid_valid(containerid):
    # Todo: allowed_characters need to be checked with runc
    allowed_characters = '^[a-zA-Z0-9_-]+$'

    result = bool(re.match(allowed_characters, containerid))

    if not result:
        print("invalid id format:", containerid)

    return True
'''