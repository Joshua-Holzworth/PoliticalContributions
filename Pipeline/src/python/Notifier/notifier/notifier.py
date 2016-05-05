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
import json
import re

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
PARAMS = "Params"
TRIGGER_SECTION = 'TriggerEvent'
TRIGGER_SCRIPT = 'TriggerScript'
SCRIPT_PARAMS = 'TriggerScriptParams'
#In long milliseconds
TRIGGER_DELAY = 'TriggerDelay'


EVENT_SCRIPT = 'EventScript'
EVENT_SECTION = 'Event'

delay=5
global parameters


def obtainQueue(maxSize):
	q = Queue(maxSize)
	return q

def parseJson(jsonLiteral):
	jsonDict = json.loads(jsonLiteral)
	return jsonDict

def generateParameters(config):
	global parameters
	parameters = dict()
	for section in config.sections():
		#print section
		sectionDict = dict(config.items(section))
		if 'val' in sectionDict:
			parameters[section] = str(sectionDict['val'])
			#print sectionDict['val']
		elif 'script' in sectionDict:
			script = sectionDict['script']
			params = ""
			if 'params' in sectionDict:
				params = sectionDict['params']
			paramCmd = 'python ' + script + ' ' + params
			#print "Running command: " + paramCmd
			paramVal = getScriptResult(paramCmd)
			parameters[section] = str(paramVal).strip()
			#print "ParamVal: "+ paramVal
	return

def printParameters(paramDict):
	for key in paramDict:
		print str(key)
		print paramDict[key]


def getScriptResult(cmd):
	proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	output,error = proc.communicate()
	return output

def loadParameters(parameters, jsonLiteral):
	print "LITERAL!" + jsonLiteral
	jsonDict = parseJson(jsonLiteral)
	newParams = parameters.copy()
	newParams.update(jsonDict)
	return newParams

paramRegx = "\$(\w+)\s*"
def replaceVarInParams(paramDict,paramLiteral):
	print("Finding params inside: "+paramLiteral)
	paramMatches = re.findall(paramRegx,paramLiteral,re.M|re.I)
	for paramMatch in paramMatches:
		paramLiteral = re.sub("\$"+paramMatch, str(paramDict[paramMatch]),paramLiteral)
	print("Final paramLiteral : "+paramLiteral)
	return paramLiteral

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
	elif config.has_option(TRIGGER_SECTION,TRIGGER_SCRIPT):
		setupScriptTrigger()
	else:
		print('FAILURE')

def startEventScript(paramDict):
	printParameters(paramDict)
	eventScript = config.get(EVENT_SECTION,EVENT_SCRIPT)
	eventParamLiteral = config.get(EVENT_SECTION,PARAMS)
	eventParams = replaceVarInParams(paramDict,eventParamLiteral)
	eventCmd = "python3 " + eventScript + " "+eventParams

	rc = subprocess.call(eventCmd,shell=True,stdout=subprocess.PIPE)
	print("EVENT CMD : "+eventCmd + " rc: " +str(rc))
	return rc


USHER_SECTION = "Usher"
USHER_SCRIPT = "UsherScript"
def executeUsherScript(paramDict):
	usherScript = config.get(USHER_SECTION,USHER_SCRIPT)
	usherParamLiteral = config.get(USHER_SECTION,PARAMS)
	usherParams = replaceVarInParams(paramDict,usherParamLiteral)
	usherCmd = "python3 " + usherScript + " " + usherParams
	rc = subprocess.call(usherCmd,shell=True,stdout=subprocess.PIPE)
	print("Ushering: " +usherCmd)

#Sets up the trigger expecting a return code of 0 from the script found in the config file
#Also sends in the config script parameters
def setupScriptTrigger():
	print('Setting up trigger based on Script!')
	global delay
	if config.has_option(TRIGGER_SECTION,PARAMS):
		if config.has_option(TRIGGER_SECTION,TRIGGER_DELAY):
			delay = float(config.get(TRIGGER_SECTION,TRIGGER_DELAY))
		scriptParamsLiteral = config.get(TRIGGER_SECTION,PARAMS)
		scriptParams = replaceVarInParams(parameters,scriptParamsLiteral)
		script = config.get(TRIGGER_SECTION,TRIGGER_SCRIPT)
		cmd = "python3 " + script+" "+scriptParams
			
		while True:
			triggerProc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			#print triggerProc
			output,error = triggerProc.communicate()
			#print "OUTPUT" + output
			print(output)
			jsonData = parseJson(output)
			if 'triggered' in jsonData:
				generateParameters(config)
				eventParams = loadParameters(parameters,output)
				if jsonData['triggered']:
					eventRC = startEventScript(eventParams)
					eventParams.update({'EventRC':eventRC})
					if eventRC == 0:
						executeUsherScript(eventParams)
						
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


def usage():
	print('notifier.py -n <name> -c <?configs?>')

def main():
	configDir = None
	name = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hn:c:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-n", "--name"):
			name = arg
		elif opt in ("-c", "--configs"):
			configDir = arg

	if configDir is not None and name is not None:
		configs = listDirectory(configDir)
		for cfg in configs:
			loadConfig(configDir+cfg)
	else:
		usage()
		sys.exit(0)
	if config is not None:
		generateParameters(config)
	printParameters(parameters)

	setupTrigger()





if __name__ == "__main__":
	exit(main())


