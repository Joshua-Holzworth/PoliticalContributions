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

#Usage
#Needs a batchID
def printHelp():
	print('stop.py -b <batchID>')

#Obtains a batchID from the arguments
#Checks to see if a process with the given batchID can be found
#Then proceeds to kill that process if found
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
	healthProc = subprocess.Popen('python '+HEALTH_CHECK_SCRIPT+ ' -b '+batchID,stdout=subprocess.PIPE,shell=True)
	output = healthProc.communicate()[0]
	pid = int(output.strip())
	if pid is not -1:
		kill_cmd = KILL_CMD + str(pid)
		killProc = subprocess.Popen(kill_cmd,shell=True)
		killProc.communicate()
		logging.warn("Command killed "+str(pid))
	else:
		logging.info("Service isn't running.")
	
if __name__ == "__main__":
	exit(main())
