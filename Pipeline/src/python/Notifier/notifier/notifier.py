#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
##            Garrett Holbrook
#####
import os
import argparse
import time
import json
import re
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import src.python.utils as utils

CFG_FILE_EXTENSION = '.cfg'

def main():
    parameters = None
    name, config_dir = parse_args()

    configs = utils.list_directory(config_dir, file_extension=CFG_FILE_EXTENSION)

    config = configparser.ConfigParser()
    for cfg in configs:
        load_config(config, config_dir + cfg)

    parameters = generate_parameters(config)
    log_parameters(parameters)

    setup_trigger(config, parameters)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--name', required=True)
    argparser.add_argument('-c', '--config-dir', required=True)

    command_args = argparser.parse_args()
    return command_args.name, command_args.config_dir

#Reads in valus into the config
#  config_file_name - The file name where configs that want to be loaded are held
#It should be noted this can be called multiple times and the order the function is called
#determines if a value inside the config is overriden.
def load_config(config, config_file_name):
    utils.log("Reading in config file: " + config_file_name, level=utils.WARN)
    config.read(config_file_name)
    
#Boots up a new script and starts it on another process
#This should be called when an event is triggered
#  scriptName - The script to be started
#  parameters - The parameters that are going to be passed into the script that's invoked
def startScript(scriptName, parameters):
    subprocess.Popen(scriptName + " " + parameters)

PARAMS = "Params"
TRIGGER_SECTION = 'TriggerEvent'
TRIGGER_SCRIPT = 'TriggerScript'
SCRIPT_PARAMS = 'TriggerScriptParams'
#In long milliseconds
TRIGGER_DELAY = 'TriggerDelay'


EVENT_SCRIPT = 'EventScript'
EVENT_SECTION = 'Event'

delay = 5

def obtain_queue(maxSize):
    q = Queue(maxSize)
    return q

def parse_json(json_literal):
    json_dict = json.loads(json_literal)
    return json_dict

def generate_parameters(config):
    parameters = dict()

    for section in config.sections():
        section_dict = dict(config.items(section))

        if 'val' in section_dict:
            parameters[section] = str(section_dict['val'])
        elif 'script' in section_dict:
            param_script = section_dict['script']
            param_script_params = ""

            if 'params' in section_dict:
                param_script_params = section_dict['params']

            command = './' + script + ' ' + param_script_params
            param_val = get_script_result(command)
            parameters[section] = str(param_val).strip()

    return parameters

def log_parameters(param_dict):
    utils.log('Parameters...')
    for key in param_dict:
        utils.log(str(key) + ': ' + str(param_dict[key]))

def get_script_result(command):
    proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    output,error = proc.communicate()
    return output

def load_parameters(parameters, json_literal):
    utils.log("LITERAL!" + json_literal)
    json_dict = parse_json(json_literal)
    newParams = parameters.copy()
    newParams.update(json_dict)
    return newParams

paramRegx = "\$(\w+)\s*"
def replace_var_in_params(param_dict, param_literal):
    utils.log("Finding params inside: " + param_literal)
    param_matches = re.findall(paramRegx, param_literal, re.M|re.I)

    for param_match in param_matches:
        param_literal = re.sub("\$" + param_match, str(param_dict[param_match]), param_literal)

    utils.log("Final param_literal : " + param_literal)

    return param_literal

#References the configuration files pulled in. 
#If the TRIGGER_SECTION described above does not exist then 
#this process will fail
#After that checks in this order
#Files exists under the TRIGGER_SECTION
#    Assuming this is true then it'll create a file watcher
#    When these files exist event will be fired and the next script will go off
#TriggerScript exists under TRIGGER_SECTION
#    Runs this script and checks for a 0 output
#    Runs on a given time (expecting a delay to be set if not a default delay will be used)
#Does not return anything just creates the trigger process and waits for this notifier to be started
def setup_trigger(config, parameters):
    if not config.has_section(TRIGGER_SECTION):
        utils.log('No trigger section in configs consumed. Shutting down process.')
    elif config.has_option(TRIGGER_SECTION, TRIGGER_SCRIPT):
        setup_script_trigger(config, parameters)
    else:
        utils.log('FAILURE', level=utils.ERROR)

def start_event_script(param_dict):
    log_parameters(param_dict)
    eventScript = config.get(EVENT_SECTION,EVENT_SCRIPT)
    eventParamLiteral = config.get(EVENT_SECTION,PARAMS)
    event_params = replace_var_in_params(param_dict,eventParamLiteral)
    eventCmd = "./" + eventScript + " "+event_params

    rc = subprocess.call(eventCmd,shell=True,stdout=subprocess.PIPE)
    utils.log("EVENT CMD : "+eventCmd + " rc: " +str(rc))
    return rc


USHER_SECTION = "Usher"
USHER_SCRIPT = "UsherScript"
def execute_usher_script(param_dict):
    usher_script = config.get(USHER_SECTION, USHER_SCRIPT)
    usher_param_literal = config.get(USHER_SECTION, PARAMS)
    usher_params = replace_var_in_params(param_dict, usher_param_literal)
    usher_command = "./" + usher_script + " " + usher_params
    rc = subprocess.call(usher_command, shell=True, stdout=subprocess.PIPE)
    utils.log("Ushering: " + usher_command)

#Sets up the trigger expecting a return code of 0 from the script found in the config file
#Also sends in the config script parameters
def setup_script_trigger(config, parameters):
    utils.log('Setting up trigger based on Script!')
    global delay

    if config.has_option(TRIGGER_SECTION, PARAMS):
        if config.has_option(TRIGGER_SECTION, TRIGGER_DELAY):
            delay = float(config.get(TRIGGER_SECTION, TRIGGER_DELAY))

        script_params_literal = config.get(TRIGGER_SECTION, PARAMS)
        script_params = replace_var_in_params(parameters, script_params_literal)
        script = config.get(TRIGGER_SECTION, TRIGGER_SCRIPT)
        command = script + " " + script_params
            
        while True:
            exit_code, stdout, stderr = utils.capture_command_output(command)
            utils.log('Command: ' + command + ' exited with code ' + 
                      str(exit_code) + '\tstdout=' + stdout + '\tstderr=' +
                      stderr, level=utils.INFO)

            if exit_code == 0:
                json_data = parse_json(stdout)

                if 'triggered' in json_data:
                    generate_parameters(config)
                    event_params = load_parameters(parameters, stdout)

                    if json_data['triggered']:
                        event_rc = start_event_script(event_params)
                        event_params.update({'EventRC':event_rc})

                        if event_rc == 0:
                            execute_usher_script(event_params)
                        
            time.sleep(delay)

#Start Trigger process
#This will encapsolate the fact that it's a process
#It'll need a directory and a file or files it's looking for before it's starts it's script
#It can even take a script or function that must return a boolean for the script to be booted up
if __name__ == "__main__":
    exit(main())
