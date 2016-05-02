#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import ConfigParser
import subprocess
import sys
import getopt
import start
import stop


global config 
config = None

def loadConfig(configFileName):
	print "Reading in config file: "+configFileName
	global config
	if config == None:
		config = ConfigParser.ConfigParser()
	config.read(configFileName)
	start.loadConfig(configFileName)
	stop.loadConfig(configFileName)


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
				stop.killNotifier(section)
				start.setupNotifier(section)
	else:
		stop.killNotifier(notifierName)
		start.setupNotifier(notifierName)


if __name__ == "__main__":
	exit(main())
