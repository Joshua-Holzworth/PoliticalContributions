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

def running_step(step_name):
    if step_running(step_name) is not 'Running':
        config.set(step_name,STATUS,'Running')

def start_step(step_name):
    if step_running(step_name) is not 'Running':
        config.set(step_name,STATUS,'Started')

def stop_event(step_name):
    config.set(step_name,STATUS,'Stopped')

def finish_event(step_name):
    config.set(step_name,STATUS,'Finished')

def write_config(config_file_name):
    with open(config_file_name,'w') as configfile:
        config.write(configfile)

def step_running(step_name):
    return config.get(step_name,STATUS)

def get_batch_id(step_name):
    return config.get(step_name,BATCHID)

def increment_batch_id(step_name):
    batch_id = int(config.get(step_name, BATCHID))
    batch_id = batch_id + 1
    config.set(step_name, BATCHID, str(batch_id))

