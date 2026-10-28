#CLI shell protoripe

import getpass
import socket
import os

#return promt based on OS username and hostname
def get_promt() -> str:
    username = getpass.getuser()
    hostname = socket.gethostname()
    cur_dir = os.getcwd()
    return f"{username}@{hostname}:{cur_dir}> "

def 
