#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####


import ConfigParser
STATUS = 'status'
BATCHID = 'batchid'

global config
config = None
def readConfig(configFileName):
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
		config.read(configFileName)


def startStep(stepName):
	if stepRunning(stepName) is not 'Running':
		config.set(stepName,STATUS,'Running')

def stopEvent(stepName):
	config.set(stepName,STATUS,'Stopped')

def finishEvent(stepName):
	config.set(stepName,STATUS,'Finished')

def writeConfig(configFileName):
	with open(configFileName,'w') as configfile:
		config.write(configfile)

def stepRunning(stepName):
	return config.get(stepName,STATUS)

def getBatchID(stepName):
	return config.get(stepName,BATCHID)

def incrBatchID(stepName):
	batchid = int(config.get(stepName,BATCHID))
	batchid = batchid + 1
	config.set(stepName,BATCHID,batchid)

