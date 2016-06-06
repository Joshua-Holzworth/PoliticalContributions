########
##    Author: Garrett Holbrook
########
import sys

import src.python.utils as utils

def build_hive_command(hql_path, param_dict):
    param_string = ''
    for key in param_dict:
        param_string += ' --hiveconf ' + str(key) + '=' + str(param_dict[key])

    return 'hive -f ' + hql_path + param_string

LOGGING_NAME = 'HqlRunner'

class HqlRunner():
    def __init__(self, parent_name, log_location, exit_on_fail=False,
                 fail_on_stdout=False, fail_on_stderr=False):
        self.logging_name = parent_name + ' ' + LOGGING_NAME
        self.log_location = log_location
        self.exit_on_fail = exit_on_fail
        self.fail_on_stdout = fail_on_stdout
        self.fail_on_stderr = fail_on_stderr

    def run(self, hql, fail_message='', **kwargs):
        hive_command = build_hive_command(hql, kwargs)
    
        exit_code, stdout, stderr = utils.capture_command_output(hive_command)
        utils.log('HiveCMD: ' + hive_command, self.logging_name, utils.INFO,
                  self.log_location)
    
        if self.exit_on_fail:
            self._fail_test(exit_code, stdout, stderr, fail_message)
    
        return exit_code, stdout, stderr

    def _fail_test(self, exit_code, stdout, stderr, fail_message):
        if self.fail_on_stderr:
            if stderr.strip():
                self._fail(exit_code, stdout, stderr, fail_message)

        if self.fail_on_stdout:
            if stdout.strip():
                self._fail(exit_code, stdout, stderr, fail_message)
     
        if exit_code:
            self._fail(exit_code, stdout, stderr, fail_message)

    def _fail(self, exit_code, stdout, stderr, fail_message):
        if fail_message:
            utils.log(fail_message, self.logging_name, utils.ERROR, self.log_location)

        print(stdout)
        utils.print_stderr(stderr)
        sys.exit(exit_code)
