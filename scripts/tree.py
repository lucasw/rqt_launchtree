#!/usr/bin/env python
# Lucas Walter

import sys

import rospkg
from rqt_launchtree.launchtree_config import LaunchtreeArg
from rqt_launchtree.launchtree_config import LaunchtreeConfig
from rqt_launchtree.launchtree_loader import LaunchtreeLoader


def path_to_package_and_launch_file(path):
    tokens = path.split("/launch/")
    package = tokens[0].split("/")[-1]
    launch = tokens[-1]
    return package, launch


def display_config_tree(config_tree, package="", launch_file="", prefix="", single_line=True, print_args=True):
    arg_text = ""
    launch_text = f"{prefix}{package} {launch_file}"
    if print_args:
        launch_text = "\n" + launch_text

    subdicts = {}
    if not single_line and package != "":
        print(f"{launch_text}")

    for key, instance in config_tree.items():
        if key == '_root':
            # print(f"{prefix} {key} {instance}")
            continue
        if isinstance(instance, dict):
            subdicts[key] = instance
        if isinstance(instance, LaunchtreeArg):
            if print_args:
                arg = instance
                if arg.value is not None:
                    pair = f"{arg.name}:={arg.value}"
                    if not single_line:
                        print(f"{prefix}    {pair}")
                    else:
                        arg_text += f" {pair}"
    if arg_text != "":
        print(f"{launch_text}{arg_text}")

    for key, instance in subdicts.items():
        package = ""
        launch_file = ""
        if ":" in key:
            filename = key.split(":")[0]
            if filename.endswith(".launch"):
                package, launch_file = path_to_package_and_launch_file(filename)
        display_config_tree(instance, package, launch_file, prefix + "  ", single_line, print_args)


if __name__ == "__main__":
    package = sys.argv[1]
    launch_file = sys.argv[2]
    launch_args = sys.argv[3:]

    rospack = rospkg.RosPack()
    path = rospack.get_path(package)
    filename = path + "/launch/" + launch_file

    launch_config = LaunchtreeConfig()
    loader = LaunchtreeLoader()
    loader.load(filename, launch_config, verbose=False, argv=["", "", ""] + launch_args)
    print(f"\n{package} {launch_file} {' '.join(launch_args)}")
    # single_line is ugly but easier to cut and paste into a command line
    display_config_tree(launch_config.tree, "", "", "  ", single_line=False, print_args=True)
