#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
##            Garrett Holbrook
#####
import os
import argparse
try:
    from configparser import ConfigParser
except ImportError:
    import ConfigParser

import src.python.utils as utils

config = None

NOTIFIER_CFG = 'cfgDir'
NOTIFIER_RELATIVE_SCRIPT = 'Notifier/notifier/notifier.py'

def main():
    config_file_name = parse_args()

    load_config(config_file_name)

    create_notifiers()

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)

    return argparser.parse_args().config_file_name

def load_config(config_file_name):
    utils.log("Reading in config file: " + config_file_name)

    global config
    if config == None:
        config = ConfigParser.ConfigParser()

    config.read(config_file_name)
    
def create_notifiers():
    utils.log("Creating notifiers")

    for section in config.sections():
        utils.log('Section: ' + str(section))

        if config.has_option(section, NOTIFIER_CFG):
            notifier_params = '-n ' + section + ' -c ' + config.get(section, NOTIFIER_CFG)
            notifier_command = './' + NOTIFIER_RELATIVE_SCRIPT + ' ' + notifier_params

            print('Running: ' + notifier_command)
            utils.run_command(notifier_command)

if __name__ == "__main__":
    exit(main())
