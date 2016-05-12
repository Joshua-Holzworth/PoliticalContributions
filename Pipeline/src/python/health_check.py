#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

import src.python.utils as utils
import notifier.utils as notifier_utils

def main():
    args = parse_args()
    config = utils.load_config(args.config_file_name)

    for section in config.sections():
        if section != 'Pipeline':
            notifier = notifier_utils.obtain_notifier(section)
            notifier = notifier.strip()
            print(section + ' : '+ ('Running' if notifier else 'Not running'))

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)

    return argparser.parse_args().config_file_name

if __name__ == '__main__':
    exit(main())
