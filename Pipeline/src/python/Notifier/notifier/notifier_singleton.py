#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
try:
    import configparser
except:
    import ConfigParser as configparser
import os

STATUS = 'status'
BATCHID = 'batchid'

global config
config = None
def read_config(config_file_name):
    global config
    if config == None:
        config = configparser.ConfigParser()
        config.read(config_file_name)

def running_step(stepName):
    if step_running(stepName) is not 'Running':
        config.set(stepName,STATUS,'Running')

def start_step(stepName):
    if step_running(stepName) is not 'Running':
        config.set(stepName,STATUS,'Started')

def stop_event(stepName):
    config.set(stepName,STATUS,'Stopped')

def finish_event(stepName):
    config.set(stepName,STATUS,'Finished')

def write_config(config_file_name):
    with open(config_file_name,'w') as configfile:
        config.write(configfile)

def step_running(stepName):
    return config.get(stepName,STATUS)

def get_batch_id(stepName):
    return config.get(stepName,BATCHID)

def incr_batch_id(stepName):
    batchid = int(config.get(stepName,BATCHID))
    batchid = batchid + 1
    config.set(stepName,BATCHID,str(batchid))

