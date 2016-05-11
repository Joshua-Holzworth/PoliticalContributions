#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse

import src.python.utils as utils
import notifier.utils as notifier_utils

def main():
    config_file_name, notifier_name, all_notifiers = parse_args()

    config = utils.load_config(config_file_name)

    if all_notifiers:
        for section in config.sections():
            if section != "Pipeline":
                kill_notifier(section)
    else:
        if config.has_section(notifier_name):
            kill_notifier(notifier_name)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-n', '--notifier-name')
    argparser.add_argument('-a', help='Restart all notifiers')

    args = argparser.parse_args()

    if not args.notifier_name and not args.a:
        argparser.error('Must specify either -n or -a option')

    return args.config_file_name, args.notifier_name, args.a

def kill_notifier(notifier_name):
    notifier_info = notifier_utils.obtain_notifier(notifier_name)

    if notifier_info:
        kill_command = 'kill -9 ' + notifier_info.split()[1]

        print('Killing ' + notifier_name + ' with command ' + command)

        utils.run_command(kill_command)

if __name__ == "__main__":
    exit(main())
