import os
import getpass
import subprocess
import shlex

def log(message, **kwargs):
    print(message)

def run_command(command):
    # see http://stackoverflow.com/questions/6466711/what-is-the-return-value-of-os-system-in-python/35362488#35362488
    return os.system(command) >> 8

def capture_command_output(command):
    PIPE = subprocess.PIPE
    process = subprocess.run(shlex.split(command), stdout=PIPE, stderr=PIPE)
    stdout = process.stdout
    stderr = process.stderr

    if stdout:
        stdout = stdout.decode('utf-8')
    if stderr:
        stderr = stderr.decode('utf-8')

    return process.returncode, stdout, stderr 

def get_user():
    return getpass.getuser()

def get_project_root_dir():
    # Gets "realpath" of this script and returns the path three levels up (the project root directory)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
