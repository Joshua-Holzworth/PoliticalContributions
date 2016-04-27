import sys

class Test:
    def __init__(self, test_name, test_func):
        self.test_name = test_name
        self.test_func = test_func

    def run(self):
        test_passed, output = self.test_func()

        if test_passed:
            print('Test "' + self.test_name + '" passed')
        else:
            print('Test "' + self.test_name + '" failed!')
            print('Output: \n')
            print(output)
            sys.exit()
