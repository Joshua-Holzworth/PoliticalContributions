#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import ConfigParser
import subprocess
import sys
import getopt

def main():
	flag = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hf:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-f"):
			flag = arg
	print "Ushering: " + flag


if __name__ == "__main__":
	exit(main())
