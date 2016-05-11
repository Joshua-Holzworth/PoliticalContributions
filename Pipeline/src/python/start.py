#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse

import src.python.utils as utils
import notifier.utils as notifier_utils

NOTIFIER_CFG = 'cfgDir'
NOTIFIER_RELATIVE_SCRIPT = 'notifier/notifier.py'

def main():
    config_file_name, notifier_name, all_notifiers = parse_args()

    config = utils.load_config(config_file_name)

    if all_notifiers:
        for section in config.sections():
            if section != "Pipeline":
                setup_notifier(section)
    else:
        if config.has_section(notifier_name):
            setup_notifier(notifier_name)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-n', '--notifier-name')
    argparser.add_argument('-a', help='Restart all notifiers')

    args = argparser.parse_args()

    if not args.notifier_name and not args.a:
        argparser.error('Must specify either -n or -a option')

    return args.config_file_name, args.notifier_name, args.a

def setup_notifier(notifier_name):
    if not notifier_utils.obtain_notifier(notifier_name):
        notifier_params = '-n ' + notifier_name + ' -c ' + config.get(notifier_name, NOTIFIER_CFG)
        notifier_command = 'python ' + NOTIFIER_RELATIVE_SCRIPT + ' ' + notifier_params

        print('Running: ' + notifier_command)

        utils.run_command(notifier_command)
    else:
        print('Notifier is already running')

if __name__ == "__main__":
    exit(main())
