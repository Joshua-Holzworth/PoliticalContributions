#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import subprocess
import sys
import getopt
import notifier_singleton


def usage():
	print('singleton_trigger.py -c <configFileName> -s <stepName> -p <previousStep>')


STATUS = 'Status'
def main():
	prevStepName = None
	stepName = None
	configFileName = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:s:p:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-c", "--configFileName"):
			configFileName = arg
		elif opt in ("-s", "--stepName"):
			stepName = arg
		elif opt in ("-p", "--prevStepName"):
			prevStepName = arg

	if stepName is None or configFileName is None:
		usage()
		sys.exit(0)

	notifier_singleton.readConfig(configFileName)
	curStatus = notifier_singleton.stepRunning(stepName)

	#Defaults to -1
	prevBatchID = -1

	if prevStepName is not None:
		prevStatus =  notifier_singleton.stepRunning(prevStepName)
		prevBatchID = int(notifier_singleton.getBatchID(prevStepName))
		if prevStatus == "Running" or prevStatus == "Stopped":
			prevBatchID = prevBatchID - 1

	triggered = True if curStatus == 'Stopped' or curStatus == 'Started' else False

	currentBatchID = int(notifier_singleton.getBatchID(stepName))

	
	triggered = triggered and (True if currentBatchID <= prevBatchID else False)
	
	if prevStatus == "Running" or prevStatus == "Stopped" and str(currentBatchID) == str(prevBatchID):
		triggered = False

	if triggered:
		notifier_singleton.runningStep(stepName)
		notifier_singleton.writeConfig(configFileName)

	batchIDJsonBlob =  "\"batchid\" : \"" + str(currentBatchID) + "\", \"batchIDMin\" : \"" + str(currentBatchID) + "\", \"batchIDMax\" : \"" + str(currentBatchID) + "\""

	jsonOutput = "{\"triggered\":" + ("true" if triggered else "false") + ", \"step\": \"" + stepName + "\", " + batchIDJsonBlob + "}"
	print(jsonOutput)
	return 0

if __name__ == "__main__":
	exit(main())