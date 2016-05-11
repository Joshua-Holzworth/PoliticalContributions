import os
import getpass
import subprocess
from subprocess import CalledProcessError
import shlex
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# logging levels
WARN = 'WARN'
INFO = 'INFO'
ERROR = 'ERROR'
DEBUG = 'DEBUG'

PIPE = subprocess.PIPE

def log(message, **kwargs):
    log_message = ''
    level = kwargs.get('level')
    name = kwargs.get('name')

    if level:
        log_message += '[' + level + '] '
    if name:
        log_message += '[' + name + '] '

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
        process = __get_last_process_in_chain(command)
        stdout, stderr = tuple(process.communicate())
        return_code = process.returncode
    except OSError as e:
        stderr = str(e)
        return_code = e.errno
    except CalledProcessError as e:
        stderr = e.output
        return_code = e.return_code

    stdout = str(stdout.decode('utf-8'))
    stderr = str(stderr.decode('utf-8'))

    return return_code, stdout, stderr 

# If there are pipes in the command, multiple process objects must be made to avoid
# the shell=True option in the Popen constructor.
def __get_last_process_in_chain(command_string):
    command_words = shlex.split(command_string)

    command_list = []
    current_command_index = 0

    # If command_string is 'ps aux | grep root | grep /usr' this loop
    # would result in [['ps', 'aux'], ['grep', 'root'], ['grep', '/usr']]
    for command_word in command_words:
        if command_word != '|':
            if len(command_list) <= current_command_index:
                command_list.append([])

            command_list[current_command_index].append(command_word)
        else:
            current_command_index += 1

    process_list = []
    process_list.append(subprocess.Popen(command_list[0], 
                                         stdout=PIPE, stderr=PIPE))

    for i in range(1, len(command_list)):
        command = command_list[i]
        process_list.append(subprocess.Popen(command, stdout=PIPE,
                            stdin = process_list[i - 1].stdout, stderr=PIPE))

    return process_list[-1]

def load_config(config_file_path, config=None):
    if not config:
        config = configparser.ConfigParser()

    config.read(config_file_path)

    return config

def get_user():
    return getpass.getuser()

def get_project_root_dir():
    # Gets "realpath" of this script and returns the path three levels up (the project root directory)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
