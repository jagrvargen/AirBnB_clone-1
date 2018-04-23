#!/usr/bin/python3
"""
   This module contains the functions, deploy, do_pack, and do_deploy
"""
from fabric.api import *
from datetime import datetime
from pathlib import Path

env.hosts = ["52.200.24.63", "54.144.25.175"]
env.user = "ubuntu"


def do_pack():
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive = "web_static_" + timestamp + ".tgz"

    local("mkdir -p versions")
    local("tar -cvzf versions/{} web_static/".format(archive))

    my_file = Path("versions/{}".format(archive))
    if my_file.is_file():
        return my_file
    else:
        return None


def do_deploy(archive_path):
    if not archive_path:
        return False

    path_name = archive_path[:-4]
    file_name = archive_path[9:]

    try:
        # Change to the tmp directory and upload the .tgz file.
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the directory to archive the .tgz file into.
        sudo("mkdir -p /data/web_static/releases/{}/".format(path_name))

        # Uncompress the zip file into the directory.
        sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            file_name, path_name))

        # Delete the archive
        sudo("rm  /tmp/{}".format(file_name))

        # Move all previous static content to new directory and remove old one.
        sudo("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(path_name, path_name))
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(
            path_name))

        # Delete old symbolic link and create a new one.
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current"
             .format(path_name))

        print("New version deployed!")
        return True

    except:
        return False


def deploy():
    # Call the do_pack function which creates a tar file from the
    # web_static package and return the path to archiveand check that
    # it exists.
    archive = do_pack()

    if archive is None:
        return False

    # Call the do_deploy function which deploys the .tgz archive to
    # two web servers and return its value (True or False).
    archive_path = str(archive)
    env.hosts = ["52.200.24.63", "54.144.25.175"]
    return do_deploy(archive_path)
