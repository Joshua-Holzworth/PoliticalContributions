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
	print("Reading in config file: "+configFileName)
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
	config.read(configFileName)

	
def usage():
	print("health_check.py -c <ConfigFileName>")



def getCommandOutput(cmd):
	proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,error = proc.communicate()
	return output

def obtainNotifier(notifierName):
	processFindCmd = "ps aux | grep [n]otifier | grep "+notifierName
	procResults = getCommandOutput(processFindCmd)
	return procResults

CFG_DIR = 'cfgDir'

def main():
	configFileName = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-c", "--configFileName"):
			configFileName = arg

	if configFileName is not None:
		loadConfig(configFileName)
	else:
		usage()
		sys.exit(0)

	for section in config.sections():
		if section != "Pipeline":
			notifier = obtainNotifier(section)
			notifier = notifier.strip()
			print(section + " : "+ ("Running" if notifier else "Stopped"))





if __name__ == "__main__":
	exit(main())
