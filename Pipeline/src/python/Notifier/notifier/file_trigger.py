#!/usr/bin/python
#######
##	Author: Joshua Holzworth
#######

import getopt
import sys
from sys import argv
import os


def printHelp():
	print 'file_trigger.py -f <file>'

def main():
	fileToWatch = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hf:")
	except getopt.GetoptError:
		printHelp()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit(2)
		elif opt in ("-f", "--file"):
			fileToWatch = arg
	fileSet = fileToWatch is not None
	rc = 3
	if fileSet:
		exists = os.path.exists(fileToWatch)
		rc = 0 if exists else 1

	jsonOutput = "{\"triggered\":" + ("true" if exists else "false") + ", \"Parameter1\":\"override!\"}"
	print jsonOutput

	return rc

if __name__ == "__main__":
	exit(main())