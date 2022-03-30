import subprocess

USER = ''
SERVER = ''
PATH = ''
FILE = './local_file.log'
RURL = "{}@{}:{}".format(USER,SERVER,PATH)

subprocess.run(["scp", RURL , FILE ])
