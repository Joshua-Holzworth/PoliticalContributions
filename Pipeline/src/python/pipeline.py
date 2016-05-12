#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
##            Garrett Holbrook
#####
import os
import argparse

import src.python.utils as utils

NOTIFIER_CFG = 'cfgDir'
NOTIFIER_RELATIVE_SCRIPT = 'notifier/notifier.py'
LOGGING_NAME = 'pipeline.py'

def main():
    config_file_name = parse_args()

    utils.log('Reading in config file: ' + config_file_name, level=utils.INFO,
              name=LOGGING_NAME)
    config = utils.load_config(config_file_name)

    create_notifiers(config)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)

    return argparser.parse_args().config_file_name

def create_notifiers(config):
    utils.log('Creating notifiers', level=utils.INFO, name=LOGGING_NAME)

    for section in config.sections():
        utils.log('Section: ' + str(section), level=utils.DEBUG,
                  name=LOGGING_NAME)

        if config.has_option(section, NOTIFIER_CFG):
            notifier_params = '-n ' + section + ' -c ' + config.get(section, NOTIFIER_CFG)
            notifier_command = NOTIFIER_RELATIVE_SCRIPT + ' ' + notifier_params

            utils.log('Running notifier with command: ' + notifier_command,
                      level=utils.INFO, name=LOGGING_NAME)
            utils.run_command(notifier_command)

if __name__ == '__main__':
    exit(main())
