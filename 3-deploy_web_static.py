#!/usr/bin/python3
"""
   This module contains a Fabric script which creates and distributes an
   archive to two web servers.
"""
from fabric.api import *
do_pack = __import__("1-pack_web_static").do_pack
do_deploy = __import__("2-do_deploy_web_static").do_deploy

env.hosts = ["52.200.24.63", "54.144.25.175"]
env.user = "ubuntu"


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
    result = do_deploy(archive_path)

    return result
