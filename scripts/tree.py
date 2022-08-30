#!/usr/bin/env python
# Lucas Walter

import sys

import rospkg
from rqt_launchtree.launchtree_config import LaunchtreeConfig
from rqt_launchtree.launchtree_loader import LaunchtreeLoader


def path_to_package_and_launch_file(path):
    tokens = path.split("/launch/")
    package = tokens[0].split("/")[-1]
    launch = tokens[-1]
    return package, launch


def display_config_tree(config_tree, prefix=""):
    for key, instance in config_tree.items():
        if key == '_root':
            # print(f"{prefix} {key} {instance}")
            continue
        if isinstance(instance, dict):
            if ":" in key:
                filename = key.split(":")[0]
                if filename.endswith(".launch"):
                    package, launch = path_to_package_and_launch_file(filename)
                    # TODO(lucasw) optionally print launch args
                    print(f"{prefix}{package} {launch}")
            display_config_tree(instance, prefix + "  ")
        # if isinstance(instance, roslaunch.core.Node):


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
    print(f"{package} {launch_file} {' '.join(launch_args)}")
    display_config_tree(launch_config.tree, "  ")
