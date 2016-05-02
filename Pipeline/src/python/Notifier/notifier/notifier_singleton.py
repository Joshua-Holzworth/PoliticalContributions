#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####


import ConfigParser
STATUS = 'Status'

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

def finishEvent(stepName):
	config.set(stepName,STATUS,'Stopped')

def writeConfig(configFileName):
	with open(configFileName,'w') as configfile:
		config.write(configfile)

def stepRunning(stepName):
	return config.get(stepName,STATUS)

