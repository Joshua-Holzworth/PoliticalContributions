import os
import getpass
import subprocess
import shlex

def run_command(command):
    subprocess.run(shlex.split(command))

def capture_command_output(command):
    process = subprocess.run(shlex.split(command), stderr=subprocess.PIPE)
    stdout = process.stdout
    stderr = process.stderr

    if stdout:
        stdout = stdout.decode('utf-8')
    if stderr:
        stderr = stderr.decode('utf-8')

    return stdout, stderr

def get_user():
    return getpass.getuser()

def get_project_root_dir():
    # Gets "realpath" of this script and returns the path three levels up (the project root directory)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
