import src.python.utils as utils

def obtain_notifier(notifier_name):
    process_find_command = 'ps aux | grep [n]otifier | grep ' + notifier_name

    exit_code, stdout, stderr = utils.capture_command_output(process_find_command)

    return stdout
