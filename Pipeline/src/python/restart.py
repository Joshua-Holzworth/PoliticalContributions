#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse

import src.python.utils as utils

START_SCRIPT_RELATIVE_PATH = 'start.py'
STOP_SCRIPT_RELATIVE_PATH = 'stop.py'

def main():
    config_file_name, notifier_name, all_notifiers = parse_args()

    config = utils.load_config(config_file_name)

    if all_notifiers:
        for section in config.sections():
            if section != "Pipeline":
                stop_notifier(config_file_name, section)
                start_notifier(config_file_name, section)
                print('')
    else:
        if config.has_section(notifier_name):
            stop_notifier(config_file_name, notifier_name)
            start_notifier(config_file_name, notifier_name)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-n', '--notifier-name')
    argparser.add_argument('-a', action='store_true', help='Restart all notifiers')

    args = argparser.parse_args()

    if not args.notifier_name and not args.a:
        argparser.error('Must specify either -n or -a option')

    return args.config_file_name, args.notifier_name, args.a

def stop_notifier(config_file_name, notifier_name):
    stop_command = './' + STOP_SCRIPT_RELATIVE_PATH + ' -c ' + config_file_name

    if notifier_name:
        stop_command += ' -n ' + notifier_name

    utils.run_command(stop_command)

def start_notifier(config_file_name, notifier_name):
    start_command = './' + START_SCRIPT_RELATIVE_PATH + ' -c ' + config_file_name

    if notifier_name:
        start_command += ' -n ' + notifier_name

    utils.run_command(start_command)

if __name__ == "__main__":
    exit(main())
