#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import ConfigParser
import subprocess
import sys
import getopt


global config 
config = None

def loadConfig(configFileName):
	print "Reading in config file: "+configFileName
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
	config.read(configFileName)

	
def usage():
	print "stop.py -c <ConfigFileName> -n <NotifierName> -A <AllNotifiers--optional>"



def getCommandOutput(cmd):
	proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,error = proc.communicate()
	return output

def obtainNotifier(notifierName):
	processFindCmd = "ps aux | grep [n]otifier | grep "+notifierName
	procResults = getCommandOutput(processFindCmd)
	return procResults

def killNotifier(notifierName):
	notifierInfo = obtainNotifier(notifierName)
	if notifierInfo:
		killCmd = 'kill -9 ' + notifierInfo.split()[1]
		getCommandOutput(killCmd)

CFG_DIR = 'cfgDir'

def main():
	configFileName = None
	notifierName = None
	allNotifiers = False
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:n:A")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-c", "--configFileName"):
			configFileName = arg
		elif opt in ("-n", "--notifierName"):
			notifierName = arg
		elif opt in ("-A", "--AllNotifiers"):
			allNotifiers = True

	if configFileName is not None:
		loadConfig(configFileName)
	else:
		usage()
		sys.exit(0)

	if allNotifiers:
		for section in config.sections():
			if section != "Pipeline":
				killNotifier(section)
	else:
		if config.has_section(notifierName):
			killNotifier(notifierName)


if __name__ == "__main__":
	exit(main())
