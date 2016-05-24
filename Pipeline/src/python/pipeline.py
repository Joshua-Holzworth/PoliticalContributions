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
PIPELINE_SECTION = 'Pipeline'
PIPELINE_NAME_OPTION = 'Name'
LOG_LOCATION_OPTION = 'LogDir'
HBASE_CONNECTION_OPTION = 'HBaseConnectionString'

def main():
    config_file_name = parse_args()

    print('Reading in config file: ' + config_file_name)
    config = utils.load_config(config_file_name)

    create_notifiers(config)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)

    return argparser.parse_args().config_file_name

def create_notifiers(config):
    print('Creating notifiers, switching from stdout to logs')

    pipeline_name = config.get(PIPELINE_SECTION, PIPELINE_NAME_OPTION)
    log_location = config.get(PIPELINE_SECTION, LOG_LOCATION_OPTION)
    hbase_connection = config.get(PIPELINE_SECTION, HBASE_CONNECTION_OPTION)

    for section in config.sections():
        utils.log('Section: ' + str(section), pipeline_name, utils.DEBUG, log_location)

        if config.has_option(section, NOTIFIER_CFG):
            notifier_params = '-n ' + section + ' -c ' + config.get(section, NOTIFIER_CFG)
            notifier_params += ' -pn "' + pipeline_name + '" -log ' + log_location
            notifier_params += ' -ht ' + pipeline_name.lower() + ' -hc ' + hbase_connection
            notifier_command = NOTIFIER_RELATIVE_SCRIPT + ' ' + notifier_params

            utils.log('Running notifier with command: ' + notifier_command,
                      pipeline_name, utils.INFO, log_location)

            process = utils.run_command_async(notifier_command)
            print(section + ' on pid ' + str(process.pid))

if __name__ == '__main__':
    exit(main())
