#!/usr/bin/env python
#######
##	Author: Joshua Holzworth
#######

import subprocess
import sys
import getopt
import logging


APP_SCRIPT_NAME = 'notifier.py'
HEALTH_CHECK_SCRIPT = 'health_check.py'


#Usage
#Needs a batch ID config is also mandiatory for right now
def printHelp():
	print 'start.py -b <batchID> -c <?configs?>'

#Checks all arguments
#Expects a config directory and a batchID
#Checks to see if a notifier for the current process exists
#If there's no process it'll boot pu a new notifier process
def main():
	configDir = None
	batchID = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:b:")
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

	if batchID is None:
		printHelp()
		sys.exit(1)

	healthProc = subprocess.Popen('python '+HEALTH_CHECK_SCRIPT+ ' -b '+batchID,stdout=subprocess.PIPE,shell=True)
	output = healthProc.communicate()[0]
	pid = int(output.strip())
	if pid is -1:
		logging.info("Starting service with batchID: "+batchID)
		notifier_process = subprocess.Popen('python ' +APP_SCRIPT_NAME+ " -b " + batchID + " -c "+configDir,shell=True)
	else:
		logging.warn("Service is already running with batchID: "+batchID)

if __name__ == "__main__":
	exit(main())