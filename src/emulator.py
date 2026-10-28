#CLI shell protoripe

import getpass.getuser() from getpass
import socket.gethostname() from socket
import os.getcwd() from os

#return promt based on OS username and hostname
def get_promt() -> str:
    username = getpass.getuser()
    hostname = socket.gethostname()
    cur_dir = os.getcwd()
    return f"{username}@{hostname}:{cur_dir}> "


