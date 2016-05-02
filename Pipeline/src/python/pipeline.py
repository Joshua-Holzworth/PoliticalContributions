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


NOTIFIER_CFG = 'cfgDir'

NOTIFIER_RELATIVE_SCRIPT = 'Notifier/notifier/notifier.py'

def loadConfig(configFileName):
	print "Reading in config file: "+configFileName
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
	config.read(configFileName)
	
def usage():
	print "pipeline.py -c <ConfigFileName>"


def createNotifiers():
	print "Creating notifiers" 
	for section in config.sections():
		print section
		if config.has_option(section,NOTIFIER_CFG):
			notifierParams = '-n ' + section + ' -c ' + config.get(section,NOTIFIER_CFG)
			notifierCMD = 'python ' + NOTIFIER_RELATIVE_SCRIPT + ' ' + notifierParams
			print 'Running: ' + notifierCMD
			subprocess.Popen(notifierCMD,shell=True)

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

	createNotifiers()





if __name__ == "__main__":
	exit(main())
