# https://gist.github.com/olooney/8155400 - argparse example

from argparse import ArgumentParser
from commandline import cmd_run, cmd_list, cmd_kill


parser = ArgumentParser(prog='pyrunc.py',
                        description="performs a variety of operations on a file.",
                        epilog="(c) Bernhard Wagesreiter, use it at your own risk!",
                        # fromfile_prefix_chars='@',
                        )



commands = parser.add_subparsers(dest="command", help="commands")
parser_run = commands.add_parser("run", help="create and run a container")
parser_run.add_argument('containerID', help="create and run a container", metavar='containerID')
parser_run.add_argument('--detach', action='store_true', help="detach from the container's process")

parser_list = commands.add_parser("list", help="lists containers started by runc with the given root")
parser_list.add_argument('--quiet', action='store_true', help="display only container IDs")

parser_kill = commands.add_parser("kill", help="kill sends the specified signal (default: SIGTERM) to the container's init process")
parser_kill.add_argument('--all', action='store_true', help="send the specified signal to all processes inside the container")

#subparsers = parser.add_subparsers(help='sub command help')


#parser_run = subparsers.add_parser('run', help='help for run', dest='handler_run')
#parser_create = subparsers.add_parser('create', help='help for create')
#parser_kill = subparsers.add_parser('kill', help='help for kill')

#parser_run = run.create_subparser(parser, subparsers)
# parser_list = list.create_subparser(parser, subparsers)


#parser_create.add_argument('containerid')
#parser_create.add_argument('--bundle')


parser.add_argument('--version', action='version', version='1.0.0')
parser.add_argument('--debug', help='enable debug output for logging', action='store_true')
parser.add_argument('--log', help='set the log file path where internal debug information is written', default='/dev/null')
parser.add_argument('--log-format', help="set the format used by logs ('text' (default), or 'json')", default='text')
parser.add_argument('--root', help='root directory for storage of container state (this should be located in tmpfs)', default='root')
parser.add_argument('--criu', help='path to the criu binary used for checkpoint and restore', default='criu')
parser.add_argument('--systemd-cgroup', help='enable systemd cgroup support, expects cgroupsPath to be of form "slice:prefix:name" for e.g. "system.slice:runc:434234"', action='store_false')
parser.add_argument('--rootless', help="ignore cgroup permission errors ('true', 'false', or 'auto')", default='auto')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.command == 'run':
        cmd_run.handler_run(args)
    elif args.command == 'list':
        cmd_list.handler_list(args)
    elif args.command == 'kill':
        cmd_kill.handler_kill(args)
    else:
        parser.print_help()
