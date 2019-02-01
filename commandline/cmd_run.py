import re   # regular expression


def handler_run(args):
    print("enter handler_list")
    if args.containerID:
        print('containerID')
        run_container(args.containerID)

    if args.detach:
        print('detach')


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
