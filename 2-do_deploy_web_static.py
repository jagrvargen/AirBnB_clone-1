#!/usr/bin/python3
"""
   This module contains a function definition for do_deploy, which distributes
   an archive to web servers.
"""
from fabric.api import *


env.hosts = ["52.200.24.63", "54.144.25.175"]
env.user = "ubuntu"


def do_deploy(archive_path):
    if not archive_path:
        return False

    path_name = archive_path[:-4]
    file_name = archive_path[9:]

    try:
        # Change to the tmp directory and upload the .tgz file.
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the directory to archive the .tgz file into.
        run("mkdir -p /data/web_static/releases/{}/".format(path_name))

        # Uncompress the zip file into the directory.
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file_name, path_name))

        # Delete the archive
        run("rm  /tmp/{}".format(file_name))

        # Move all previous static content to new directory and remove old one.
        run("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(path_name, path_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            path_name))

        # Delete old symbolic link and create a new one.
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(path_name))

        print("New version deployed!")
        return True

    except:
        return False
