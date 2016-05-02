#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import getopt
import sys

def main():
	outFlag = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"f:")
	except getopt.GetoptError:
		printHelp()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-f':
			outFlag = arg
	output = 'output!'

	if outFlag is not None:
		output  = output + ' ' + outFlag
		output = output.upper()

	print output
	return 0


if __name__ == "__main__":
	exit(main())