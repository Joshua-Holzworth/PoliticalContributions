#!/usr/bin/python3 -B
#####
##	Author: Joshua Holzworth
#####


import ConfigParser
import os
import subprocess
import sys
import time
import getopt
import logging

global config 
config = None

#config = ConfigParser.ConfigParser()

#Reads in valus into the config
#  configFileName - The file name where configs that want to be loaded are held
#It should be noted this can be called multiple times and the order the function is called
#determines if a value inside the config is overriden.
def loadConfig(configFileName):
	logging.warn("Reading in config file: "+configFileName)
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
	config.read(configFileName)
	

#Boots up a new script and starts it on another process
#This should be called when an event is triggered
#  scriptName - The script to be started
#  parameters - The parameters that are going to be passed into the script that's invoked
def startScript(scriptName, parameters):
	subprocess.Popen(scriptName + " " + parameters)



#def start():

#def stop():

TRIGGER_SECTION = 'TriggerEvent'
TRIGGER_SCRIPT = 'TriggerScript'
SCRIPT_PARAMS = 'TriggerScriptParams'
#In long milliseconds
TRIGGER_DELAY = 'TriggerDelay'

delay=5

#References the configuration files pulled in. 
#If the TRIGGER_SECTION described above does not exist then 
#this process will fail
#After that checks in this order
#Files exists under the TRIGGER_SECTION
#	Assuming this is true then it'll create a file watcher
#	When these files exist event will be fired and the next script will go off
#TriggerScript exists under TRIGGER_SECTION
#	Runs this script and checks for a 0 output
#	Runs on a given time (expecting a delay to be set if not a default delay will be used)
#Does not return anything just creates the trigger process and waits for this notifier to be started
def setupTrigger():
	if config.has_section(TRIGGER_SECTION) == False:
		print('No trigger section in configs consumed. Shutting down process.')
	elif config.has_option(TRIGGER_SECTION,'Files'):
		print('Setting up trigger based on Files!')
	elif config.has_option(TRIGGER_SECTION,TRIGGER_SCRIPT):
		setupScriptTrigger()
	else:
		print('FAILURE')

#Sets up the trigger expecting a return code of 0 from the script found in the config file
#Also sends in the config script parameters
def setupScriptTrigger():
	print('Setting up trigger based on Script!')
	if config.has_option(TRIGGER_SECTION,SCRIPT_PARAMS):

		if config.has_option(TRIGGER_SECTION,TRIGGER_DELAY):
			delay = float(config.get(TRIGGER_SECTION,TRIGGER_DELAY))

		scriptParams = config.get(TRIGGER_SECTION,SCRIPT_PARAMS)
		script = config.get(TRIGGER_SECTION,TRIGGER_SCRIPT)
		cmd = "python " + script+" "+scriptParams
			
		while True:
			returnCode = subprocess.call(cmd,shell=True,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			if returnCode != 0:
				print("Invalid")
			else:
				print("TRIGGERED!")
				#Run your default script
			time.sleep(delay)


#Start Trigger process
#This will encapsolate the fact that it's a process
#It'll need a directory and a file or files it's looking for before it's starts it's script
#It can even take a script or function that must return a boolean for the script to be booted up


def listDirectory(rootDir):
	validDir = os.path.isdir(rootDir)
	if validDir == False:
		logging.error("Directory: " + rootDir + " is not a valid directory.")
	else:
		files = os.listdir(rootDir)
	return files


def printHelp():
	print('notifier.py -b <batchID> -c <?configs?>')


def main():
	configDir = None
	batchID = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hb:c:")
	except getopt.GetoptError:
		printHelp()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit(0)
		elif opt in ("-c", "--configs"):
			configDir = arg
		elif opt in ("-b","--batchID"):
			batchID = arg

	if configDir is not None:
		configs = listDirectory(configDir)
		for config in configs:
			loadConfig(configDir+config)

	setupTrigger()





if __name__ == "__main__":
	exit(main())


