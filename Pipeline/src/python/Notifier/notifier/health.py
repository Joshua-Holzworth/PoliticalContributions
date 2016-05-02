#!/usr/bin/python3 -B
#######
##	Author: Joshua Holzworth
#######

import subprocess
import sys
import getopt
import logging


APP_SCRIPT_NAME = 'notifier.py'

HEALTH_CHECK_SCRIPT = 'health_check.py'

KILL_CMD = 'kill '

def printHelp():
	print('stop.py -b <batchID>')

def main():
	batchID = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hb:")
	except getopt.GetoptError:
		printHelp()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit(0)
		elif opt in ("-b", "--batchID"):
			batchID = arg
	healthProc = subprocess.Popen('python '+HEALTH_CHECK_SCRIPT+ ' -b '+str(batchID),stdout=subprocess.PIPE,shell=True)
	output = healthProc.communicate()[0]
	pid = int(output.strip())
	if pid is not -1:
		logging.warn("Service running.")
	else:
		logging.warn("Service isn't running.")
	
if __name__ == "__main__":
	exit(main())
