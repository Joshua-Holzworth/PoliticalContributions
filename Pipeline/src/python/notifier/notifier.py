#! /usr/bin/env python
#####
##    Author: Joshua Holzworth
##            Garrett Holbrook
#####
import os
import argparse
import time
import json

from notifier_config import NotifierConfig
import src.python.utils as utils
from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

CFG_FILE_EXTENSION = '.cfg'
LOGGING_NAME = 'notifier.py'
LOG_LOCATION = None
NOTIFIER_NAME = None

def main():
    parameters = None
    args = parse_args()

    global LOGGING_NAME, LOG_LOCATION, NOTIFIER_NAME
    LOGGING_NAME = args.parent_name + ' ' + args.name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location
    NOTIFIER_NAME = args.name

    config = read_configs(args.config_dir)
    notifier_config = NotifierConfig(config, LOGGING_NAME, LOG_LOCATION)
    dal = DataAccessLayer(Connector(args.hbase_connection), args.hbase_table)

    start_step(notifier_config, parameters, dal)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--name', required=True)
    argparser.add_argument('-hc', '--hbase-connection',
                           help='HBase connection string', required=True)
    argparser.add_argument('-ht', '--hbase-table', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)
    argparser.add_argument('-c', '--config-dir', required=True)

    return argparser.parse_args()

def read_configs(config_dir):
    configs = utils.list_directory(config_dir, file_extension=CFG_FILE_EXTENSION)

    config = None
    for cfg in configs:
        config = utils.load_config(args.config_dir + '/' + cfg, config=config)

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
def start_step(notifier_config, parameters, dal):
    if not notifier_config.trigger:
        utils.log('No trigger section in configs consumed. Shutting down process.',
                  LOGGING_NAME, utils.ERROR, LOG_LOCATION)
    elif notifier_config.trigger.script:
        execute_step(notifier_config, parameters)
    else:
        utils.log('FAILURE', LOGGING_NAME, utils.ERROR, LOG_LOCATION)

# Begins the Trigger-Event-Usher loop
def execute_step(notifier_config, parameters, dal):
    utils.log('Starting Trigger-Event-Usher loop', LOGGING_NAME,
              utils.INFO, LOG_LOCATION)

    while True:
        trigger_rc, stdout, stderr = execute_trigger_script(notifier_config)

        if trigger_rc == 0:
            dal.increment_step(NOTIFIER_NAME)
            json_response = parse_json(stdout)

            if json_response.get('triggered') == 'true':
                event_successful, output = run_event(notifier_config, dal, json_response)

                if event_successful:
                    json_response = parse_json(output)
                    execute_usher_script(config, json_response)
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
        if current_attempt < notifer_config.event.retry_count and not event_successful:
            event_command = notifier_config.get_event_command(json_response)

            utils.log('Event attempt ' + str(current_attempt + 1), LOGGING_NAME,
                      utils.INFO, LOG_LOCATION)
            utils.log('Running event with command: ' + event_command, LOGGING_NAME,
                      utils.INFO, LOG_LOCATION)

            dal.set_step_to_running(NOTIFIER_NAME, event_command)
            rc, stdout, stderr = utils.capture_command_output(event_command)

            utils.log('Event with command: ' + event_command + ' returned code ' + 
                      str(rc) + ' stdout=' + stdout + ' stderr=' + stderr,
                      LOGGING_NAME, utils.INFO, LOG_LOCATION)

            if rc == 0:
                 dal.set_step_to_finished(NOTIFIER_NAME, stdout)
                 event_successful = True
                 output = stdout
            else:
                current_attempt += 1
                dal.set_step_to_finished(NOTIFIER_NAME, 
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
