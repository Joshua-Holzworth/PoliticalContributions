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
	print 'singleton_trigger.py -c <configFileName> -s <stepName>'


STATUS = 'Status'
def main():
	stepName = None
	configFileName = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:s:")
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

	if stepName is None:
		usage()
		sys.exit(0)

	notifier_singleton.readConfig(configFileName)
	curStatus = notifier_singleton.stepRunning(stepName)
	
	if curStatus == 'Stopped':
		notifier_singleton.startStep(stepName)
		notifier_singleton.writeConfig(configFileName)

	jsonOutput = "{\"triggered\":" + ("true" if curStatus == 'Stopped' else "false") + "}"
	print jsonOutput
	return 0

if __name__ == "__main__":
	exit(main())