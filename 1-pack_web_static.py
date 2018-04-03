#!/usr/bin/python3
"""
   This module contains a Fabric function definition.
"""
from datetime import datetime, time
from fabric.api import *
import tarfile
from pathlib import Path


def do_pack():
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive = "web_static_" + timestamp + ".tgz"

    local("mkdir -p versions")
    local("python3 -m tarfile -cv versions/{} web_static/".format(archive))

    my_file = Path("versions/{}".format(archive))
    if my_file.is_file():
        return my_file

    return None

if __name__ == "__main__":
    do_pack()
