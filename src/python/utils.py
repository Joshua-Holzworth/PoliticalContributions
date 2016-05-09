import os
import getpass
import subprocess
import shlex

# logging levels
WARN = 'WARN'
INFO = 'INFO'
ERROR = 'ERROR'
DEBUG = 'DEBUG'

def log(message, **kwargs):
    log_message = ''
    level = kwargs.get('level')

    if level:
        log_message += '[' + level + '] '
    log_message += message

    print(log_message)

def list_directory(directory):
    files = []

    if os.path.isdir(directory):
        files = os.listdir(directory)
    else:
        log("Directory: " + directory + " is not a valid directory.", level=ERROR)

    return files

def run_command(command):
    # see http://stackoverflow.com/questions/6466711/what-is-the-return-value-of-os-system-in-python/35362488#35362488
    return os.system(command) >> 8

def capture_command_output(command):
    PIPE = subprocess.PIPE
    process = subprocess.Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
    stdout, stderr = tuple(process.communicate())

    if stdout:
        stdout = str(stdout.decode('utf-8'))
    if stderr:
        stderr = str(stderr.decode('utf-8'))

    return process.returncode, stdout, stderr 

def get_user():
    return getpass.getuser()

def get_project_root_dir():
    # Gets "realpath" of this script and returns the path three levels up (the project root directory)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
