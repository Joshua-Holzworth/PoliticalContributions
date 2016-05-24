#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse

import src.python.utils as utils
import notifier.utils as notifier_utils

NOTIFIER_CFG = 'cfgDir'
NOTIFIER_RELATIVE_SCRIPT = 'notifier/notifier.py'
PIPELINE_SECTION = 'Pipeline'
PIPELINE_NAME = 'Name'
LOG_LOCATION_NAME = 'LogDir'
HBASE_CONNECTION_OPTION = 'HBaseConnectionString'

def main():
    config_file_name, notifier_name, all_notifiers = parse_args()

    config = utils.load_config(config_file_name)

    parent_name = config.get(PIPELINE_SECTION, PIPELINE_NAME)
    log_location = config.get(PIPELINE_SECTION, LOG_LOCATION_NAME)
    hbase_connection = config.get(PIPELINE_SECTION, HBASE_CONNECTION_OPTION)

    if all_notifiers:
        for section in config.sections():
            if section != "Pipeline":
                setup_notifier(config, section, hbase_connection, parent_name, log_location)
    else:
        if config.has_section(notifier_name):
            setup_notifier(config, notifier_name, hbase_connection, parent_name, log_location)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-n', '--notifier-name')
    argparser.add_argument('-a', action='store_true', help='Restart all notifiers')

    args = argparser.parse_args()

    if not args.notifier_name and not args.a:
        argparser.error('Must specify either -n or -a option')

    return args.config_file_name, args.notifier_name, args.a

def setup_notifier(config, notifier_name, hbase_connection, parent_name, log_location):
    if not notifier_utils.obtain_notifier(notifier_name):
        notifier_params = '-n ' + notifier_name + ' -c ' + config.get(notifier_name, NOTIFIER_CFG)
        notifier_params += ' -pn "' + parent_name + '" -log ' + log_location
        notifier_params += ' -ht ' + parent_name.lower() + ' -hc ' + hbase_connection
        notifier_command = './' + NOTIFIER_RELATIVE_SCRIPT + ' ' + notifier_params

        print('Running: ' + notifier_command)

        utils.run_command_async(notifier_command)
    else:
        print('Notifier ' + notifier_name + ' is already running')

if __name__ == "__main__":
    exit(main())
