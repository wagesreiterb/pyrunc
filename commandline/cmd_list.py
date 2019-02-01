import os
import json
import config


def handler_list(args):
    if not args.quiet:
        # list all containers in the normal format
        print('{0:12}{1:12}{2:12}{3:35}{4:33}{5}'.format("ID", "PID", "STATUS", "BUNDLE", "CREATED", "OWNER"))
        for dirpath, dirnames, filenames in os.walk(config.path_to_containers,
                                                    onerror=walk_error_handler,
                                                    topdown=False):
            for container in dirnames:
                file_of_container_state = os.path.join(dirpath, container, config.file_of_container_state)
                with open(file_of_container_state) as json_file:
                    data = json.load(json_file)
                    bundle = get_path_to_bundle(data['config']['labels'])
                    print('{:<12}{:<12}{:<12}{:<35}{:<33}{:<}'
                          .format(container,
                                  data['init_process_pid'],
                                  "status",
                                  bundle,
                                  data['created'],
                                  "owner"))

        #for name, phone in table.items():
            #print('{0:20} ==> {1:10d}'.format(name, phone))
        #    print('{0:12}{1:12}{2:12}{3:35}{4:33}{5}'.format("ID", "PID", "STATUS", "BUNDLE", "CREATED", "OWNER"))

    else:
        # list only the names of all containers
        for dirpath, dirnames, filenames in os.walk(config.path_to_containers,
                                                    onerror=walk_error_handler,
                                                    topdown=False):
            for name in dirnames:
                print(name)


def get_path_to_bundle(labels):
    path_to_bundle = "abc"
    for label in labels:
        key, value = label.split('=')
        if key == "bundle":
            path_to_bundle = value

    return path_to_bundle


def walk_error_handler(exception_instance):
    print(exception_instance)
