#!/usr/bin/python3 -B
#######
##	Author: Joshua Holzworth
#######

import subprocess
import sys
import getopt


APP_SCRIPT_NAME = 'notifier.py'

def printHelp():
	print('health_check.py -b <batchID>')


def main():
	batchID = None
	pid = -1
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

	if batchID is not None:
		processListCmd = 'ps aux | grep python | grep [n]otifier | grep '+batchID 
		listProcess = subprocess.Popen(processListCmd,stdout=subprocess.PIPE,shell=True)
		out = listProcess.communicate()[0]
		sections = out.split()
		if len(out):
			pid = sections[1]
	print(pid)
	return pid
	
if __name__ == "__main__":
	exit(main())
