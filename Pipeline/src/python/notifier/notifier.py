#! /usr/bin/env python2.7
#####
##    Author: Joshua Holzworth
##            Garrett Holbrook
#####
import os
import argparse
import time
import json
import re

from notifier_config import NotifierConfig
import src.python.utils as utils
from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

CFG_FILE_EXTENSION = '.cfg'
LOGGING_NAME = 'notifier.py'
LOG_LOCATION = None
STEP_NAME = None
SCHEMA = {
    'current': dict(),
    'attemptStart': dict(),
    'attemptEnd': dict()
}

def main():
    args = parse_args()

    global LOGGING_NAME, LOG_LOCATION, STEP_NAME
    LOGGING_NAME = args.parent_name + ' ' + args.name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location
    STEP_NAME = args.name

    config = read_configs(args.config_dir)
    notifier_full_name = args.parent_name + ' ' + args.name
    notifier_config = NotifierConfig(config, notifier_full_name, LOG_LOCATION)
    dal = DataAccessLayer(Connector(args.hbase_connection), args.hbase_table)

    utils.log('Creating watermark table if not exists', LOGGING_NAME,
              utils.DEBUG, LOG_LOCATION)
    dal.create_table_if_not_exists(SCHEMA)

    start_step(notifier_config, dal)

# Even though all arguments are necessary for the proper functioning of
# the notifier, only log-location is set to true. See check_args for
# a further explanation
def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--name')
    argparser.add_argument('-hc', '--hbase-connection',
                           help='HBase connection string')
    argparser.add_argument('-ht', '--hbase-table')
    argparser.add_argument('-pn', '--parent-name')
    argparser.add_argument('-log', '--log-location', required=True)
    argparser.add_argument('-c', '--config-dir')

    args = argparser.parse_args()

    check_args(args, argparser)

    return args

# The --log-location arg is imperative so that if something goes wrong
# with parsing the args, the failure can be properly logged. For example, if
# all args in argparser had required=True, then if something like the
# --hbase-table arg was missing, argparser.parse_args would fail completely
# and we wouldn't have a way of properly logging that because the -log arg
# was not captured.
# With check_args, we check for the other arguments and if they are not
# present then we can properly log that issue as opposed to having argparser
# write to stderr
def check_args(arguments, argparser):
    if not (arguments.name and arguments.hbase_connection and arguments.hbase_table
               and arguments.parent_name and arguments.config_dir):

        usage = re.sub('\s+', ' ', argparser.format_usage())
        parent_name = arguments.parent_name or 'NOPARENT'
        name = arguments.name or 'NONAME'
        log_name = parent_name + ' ' + name + ' ' + LOGGING_NAME

        utils.log('FATAL Missing arguments. ' + str(usage), log_name,
                  utils.ERROR, arguments.log_location)

        raise SystemExit(usage)

def read_configs(config_dir):
    configs = utils.list_directory(config_dir, file_extension=CFG_FILE_EXTENSION)

    config = None
    for cfg in configs:
        config = utils.load_config(config_dir + '/' + cfg, config=config)

    return config

def parse_json(json_literal):
    json_dict = dict()

    try:
        json_dict = json.loads(json_literal.rstrip())
    except ValueError:
        pass

    return json_dict 
# Ensures that a trigger exists in the config before starting
# the Trigger-Event-Usher loop
def start_step(notifier_config, dal):
    if not notifier_config.trigger:
        utils.log('No trigger section in configs consumed. Shutting down process.',
                  LOGGING_NAME, utils.ERROR, LOG_LOCATION)
    elif notifier_config.trigger.script:
        execute_step(notifier_config, dal)
    else:
        utils.log('FAILURE', LOGGING_NAME, utils.ERROR, LOG_LOCATION)

# Begins the Trigger-Event-Usher loop
def execute_step(notifier_config, dal):
    utils.log('Starting Trigger-Event-Usher loop', LOGGING_NAME,
              utils.INFO, LOG_LOCATION)

    while True:
        trigger_rc, stdout, stderr = execute_trigger_script(notifier_config)

        if trigger_rc == 0:
            json_response = parse_json(stdout)
            triggered = json_response.get('triggered')

            # I'm comparing boolean constants here because if I just had 
            # 'if triggered' then if triggered was the string 'false' it would
            # evaluate to True
            if triggered == 'true' or triggered == True:
                utils.log('Incrementing step in HBase', LOGGING_NAME, utils.DEBUG,
                          LOG_LOCATION)
                dal.increment_step(STEP_NAME)
                event_successful, output = run_event(notifier_config, dal, json_response)

                if event_successful:
                    json_response = parse_json(output)
                    execute_usher_script(notifier_config, json_response)
                else:
                    pass # TODO fail somehow, alert user of event script failure
                    
        time.sleep(notifier_config.trigger.delay)

def execute_trigger_script(notifier_config):
    trigger_command = notifier_config.get_trigger_command()

    utils.log('Running trigger with command: "' + trigger_command + '" ', 
              LOGGING_NAME, utils.INFO, LOG_LOCATION)

    rc, stdout, stderr = utils.capture_command_output(trigger_command)

    utils.log('Trigger command: "' + trigger_command + '" exited with code ' + 
              str(rc) + ', stdout=' + stdout.rstrip() + ', stderr=' +
              stderr.rstrip(), 
              LOGGING_NAME, utils.INFO, LOG_LOCATION)

    return rc, stdout, stderr

# Sets the step in hbase to running and runs the event script, if the script
# fails then it will set the step to stopped with the output of the script
# and will retry it a configurable number of times. If the script returns 0
# then it will set the step to finished with the output of the script
def run_event(notifier_config, dal, json_response):
    current_attempt = 0
    event_successful = False
    output = 'Event has not been run'

    if notifier_config.event:
        if current_attempt < notifier_config.event.retry_count and not event_successful:
            event_command = notifier_config.get_event_command(json_response)

            utils.log('Event attempt ' + str(current_attempt + 1), LOGGING_NAME,
                      utils.INFO, LOG_LOCATION)
            utils.log('Setting step to "Running" in HBase', LOGGING_NAME,
                      utils.DEBUG, LOG_LOCATION)
            utils.log('Running event with command: ' + event_command, LOGGING_NAME,
                      utils.INFO, LOG_LOCATION)
            dal.set_step_to_running(STEP_NAME, event_command)
            rc, stdout, stderr = utils.capture_command_output(event_command)

            utils.log('Event with command: ' + event_command + ' returned code ' + 
                      str(rc) + ' stdout=' + stdout + ' stderr=' + stderr,
                      LOGGING_NAME, utils.INFO, LOG_LOCATION)

            if rc == 0:
                utils.log('Setting step to "Finished" in HBase', LOGGING_NAME,
                          utils.DEBUG, LOG_LOCATION)
                dal.set_step_to_finished(STEP_NAME, stdout)
                event_successful = True
                output = stdout
            else:
                utils.log('Step failed on attempt ' + str(current_attempt) + 
                          ', setting step to "Stopped" in HBase', 
                          LOGGING_NAME, utils.DEBUG, LOG_LOCATION)
                current_attempt += 1
                dal.set_step_to_stopped(STEP_NAME, 
                                         'Exit code: ' + str(rc) + ' stdout=' + 
                                         stdout + ' stderr=' + stderr)
        else:
            utils.log('Retry attempts exceeded limit of ' + 
                      str(notifier_config.event.retry_count),
                      LOGGING_NAME, utils.ERROR, LOG_LOCATION)
    else:
        event_successful = True
        output = '{}'
        utils.log('No event section found in config, skipping to usher',
                  LOGGING_NAME, utils.WARN, LOG_LOCATION)
        utils.log('Setting step to "Finished" in HBase', LOGGING_NAME,
                  utils.DEBUG, LOG_LOCATION)
        dal.set_step_to_finished(STEP_NAME)

    return event_successful, output

def execute_usher_script(notifier_config, json_response):
    usher_command = notifier_config.get_usher_command(json_response)

    utils.log('Ushering: ' + usher_command, LOGGING_NAME, utils.INFO, LOG_LOCATION)

    exit_code, stdout, stderr = utils.capture_command_output(usher_command)

    utils.log('Usher command: "' + usher_command + '" exited with code ' + 
              str(exit_code) + ', stdout=' + stdout.rstrip() + ', stderr=' +
              stderr.rstrip(), 
              LOGGING_NAME, utils.INFO, LOG_LOCATION)

    return exit_code, stdout, stderr

#This will encapsolate the fact that it's a process
#It'll need a directory and a file or files it's looking for before it's starts it's script
#It can even take a script or function that must return a boolean for the script to be booted up
if __name__ == '__main__':
    exit(main())
