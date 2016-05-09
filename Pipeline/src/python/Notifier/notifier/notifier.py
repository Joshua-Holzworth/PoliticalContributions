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

config = configparser.ConfigParser()

def main():
    parameters = None
    name, config_dir = parse_args()

    configs = utils.list_directory(config_dir)

    for cfg in configs:
        load_config(config_dir + cfg)

    parameters = generate_parameters(config)
    print_parameters(parameters)

    setupTrigger()

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--name', required=True)
    argparser.add_argument('-c', '--config-dir', required=True)

    command_args = argparser.parse_args()
    return command_args.name, command_args.config_dir

#config = ConfigParser.ConfigParser()

#Reads in valus into the config
#  config_file_name - The file name where configs that want to be loaded are held
#It should be noted this can be called multiple times and the order the function is called
#determines if a value inside the config is overriden.
def load_config(config_file_name):
    utils.log("Reading in config file: " + config_file_name, level=utils.WARN)
    config.read(config_file_name)
    

#Boots up a new script and starts it on another process
#This should be called when an event is triggered
#  scriptName - The script to be started
#  parameters - The parameters that are going to be passed into the script that's invoked
def startScript(scriptName, parameters):
    subprocess.Popen(scriptName + " " + parameters)



#def start():

#def stop():
PARAMS = "Params"
TRIGGER_SECTION = 'TriggerEvent'
TRIGGER_SCRIPT = 'TriggerScript'
SCRIPT_PARAMS = 'TriggerScriptParams'
#In long milliseconds
TRIGGER_DELAY = 'TriggerDelay'


EVENT_SCRIPT = 'EventScript'
EVENT_SECTION = 'Event'

delay = 5
global parameters


def obtainQueue(maxSize):
    q = Queue(maxSize)
    return q

def parse_json(json_literal):
    json_dict = json.loads(json_literal)
    return json_dict

def generate_parameters(config):
    parameters = dict()

    for section in config.sections():
        section_dict = dict(config.items(section))
        print(section_dict)

        if 'val' in section_dict:
            parameters[section] = str(section_dict['val'])
        elif 'script' in section_dict:
            script = section_dict['script']
            params = ""

            if 'params' in section_dict:
                params = section_dict['params']
            command = './' + script + ' ' + params
            paramVal = getScriptResult(command)
            parameters[section] = str(paramVal).strip()

    return parameters

def printParameters(paramDict):
    for key in paramDict:
        utils.log(str(key))
        utils.log(paramDict[key])


def getScriptResult(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output,error = proc.communicate()
    return output

def loadParameters(parameters, json_literal):
    utils.log("LITERAL!" + json_literal)
    json_dict = parse_json(json_literal)
    newParams = parameters.copy()
    newParams.update(json_dict)
    return newParams

paramRegx = "\$(\w+)\s*"
def replaceVarInParams(paramDict,paramLiteral):
    utils.log("Finding params inside: "+paramLiteral)
    paramMatches = _je.findall(paramRegx,paramLiteral,re.M|re.I)
    for paramMatch in paramMatches:
        paramLiteral = re.sub("\$"+paramMatch, str(paramDict[paramMatch]),paramLiteral)
    utils.log("Final paramLiteral : "+paramLiteral)
    return paramLiteral

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
def setupTrigger():
    if config.has_section(TRIGGER_SECTION) == False:
        utils.log('No trigger section in configs consumed. Shutting down process.')
    elif config.has_option(TRIGGER_SECTION,TRIGGER_SCRIPT):
        setupScriptTrigger()
    else:
        utils.log('FAILURE')

def startEventScript(paramDict):
    printParameters(paramDict)
    eventScript = config.get(EVENT_SECTION,EVENT_SCRIPT)
    eventParamLiteral = config.get(EVENT_SECTION,PARAMS)
    event_params = replaceVarInParams(paramDict,eventParamLiteral)
    eventCmd = "./" + eventScript + " "+event_params

    rc = subprocess.call(eventCmd,shell=True,stdout=subprocess.PIPE)
    utils.log("EVENT CMD : "+eventCmd + " rc: " +str(rc))
    return rc


USHER_SECTION = "Usher"
USHER_SCRIPT = "UsherScript"
def execute_usher_script(paramDict):
    usherScript = config.get(USHER_SECTION,USHER_SCRIPT)
    usherParamLiteral = config.get(USHER_SECTION,PARAMS)
    usherParams = replaceVarInParams(paramDict,usherParamLiteral)
    usherCmd = "./" + usherScript + " " + usherParams
    rc = subprocess.call(usherCmd,shell=True,stdout=subprocess.PIPE)
    utils.log("Ushering: " +usherCmd)

#Sets up the trigger expecting a return code of 0 from the script found in the config file
#Also sends in the config script parameters
def setupScriptTrigger():
    utils.log('Setting up trigger based on Script!')
    global delay
    if config.has_option(TRIGGER_SECTION,PARAMS):
        if config.has_option(TRIGGER_SECTION,TRIGGER_DELAY):
            delay = float(config.get(TRIGGER_SECTION,TRIGGER_DELAY))
        scriptParamsLiteral = config.get(TRIGGER_SECTION,PARAMS)
        scriptParams = replaceVarInParams(parameters,scriptParamsLiteral)
        script = config.get(TRIGGER_SECTION,TRIGGER_SCRIPT)
        cmd = "./" + script+" "+scriptParams
            
        while True:
            triggerProc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            #print triggerProc
            output,error = triggerProc.communicate()
            #print "OUTPUT" + output
            utils.log(output)
            json_data = parse_json(output)
            if 'triggered' in json_data:
                generate_parameters(config)
                event_params = loadParameters(parameters,output)
                if json_data['triggered']:
                    event_rc = startEventScript(event_params)
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
