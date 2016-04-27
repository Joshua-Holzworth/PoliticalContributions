import sys

import src.py3.utils as utils

class Test:
    def __init__(self, test_name, test_func):
        self.test_name = test_name
        self.test_func = test_func

    def run(self):
        test_passed, output = self.test_func()

        if test_passed:
            utils.log('Test "' + self.test_name + '" passed')
        else:
            utils.log('Test "' + self.test_name + '" failed!')
            utils.log('Output: \n')
            utils.log(output)
            sys.exit()
