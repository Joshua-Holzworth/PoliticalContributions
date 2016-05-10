import os
import getpass
import subprocess
from subprocess import CalledProcessError
import shlex

# logging levels
WARN = 'WARN'
INFO = 'INFO'
ERROR = 'ERROR'
DEBUG = 'DEBUG'

PIPE = subprocess.PIPE

def log(message, **kwargs):
    log_message = ''
    level = kwargs.get('level')

    if level:
        log_message += '[' + level + '] '
    log_message += message

    print(log_message)

def list_directory(directory, file_extension=None):
    files = []

    if os.path.isdir(directory):
        files = os.listdir(directory)
    else:
        log("Directory: " + directory + " is not a valid directory.", level=ERROR)

    if file_extension:
        files = filter(lambda x: x.endswith(file_extension), files)

    return files

def run_command(command):
    # see http://stackoverflow.com/questions/6466711/what-is-the-return-value-of-os-system-in-python/35362488#35362488
    return os.system(command) >> 8

def capture_command_output(command):
    return_code, stdout, stderr = 1, '', ''

    try:
        process = subprocess.Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
        stdout, stderr = tuple(process.communicate())
        return_code = process.returncode
    except OSError as e:
        stderr = str(e)
        return_code = e.errno
    except CalledProcessError as e:
        stderr = e.output
        return_code = e.return_code

    if stdout:
        stdout = str(stdout.decode('utf-8'))
    if stderr:
        stderr = str(stderr.decode('utf-8'))

    return return_code, stdout, stderr 

def get_user():
    return getpass.getuser()

def get_project_root_dir():
    # Gets "realpath" of this script and returns the path three levels up (the project root directory)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
