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
