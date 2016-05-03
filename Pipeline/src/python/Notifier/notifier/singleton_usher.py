#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import ConfigParser
import subprocess
import sys
import getopt

import notifier_singleton
	
def usage():
	print("singleton_usher.py -c <ConfigFileName> -s <CurrentStep> -r <CurrentStepReturnCode>")


def main():
	configFileName = None
	currentStep = None
	returnCode = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:s:r:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-c", "--configFileName"):
			configFileName = arg
		elif opt in ("-s", "--currentStep"):
			currentStep = arg
		elif opt in ("-r", "--returnCode"):
			returnCode = arg

	if configFileName == None or currentStep == None or returnCode == None:
		usage()
		exit(134)

	notifier_singleton.readConfig(configFileName)
	if notifier_singleton.stepRunning(currentStep) == "Running":
		if returnCode == "1":
			notifier_singleton.finishEvent(currentStep)
		elif returnCode == "0":
			#If this is a success
			#Then we are going to increment the currensteps batchid (Only if previous step's id is less)
			#Actually we are going to make that check in the trigger
			#We are just going to increment
			notifier_singleton.incrBatchID(currentStep)
			notifier_singleton.finishEvent(currentStep)
		notifier_singleton.writeConfig(configFileName)
	else:
		print('Nothing to usher')

if __name__ == "__main__":
	exit(main())
