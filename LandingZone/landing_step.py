#!/usr/bin/python
#######
##	Author Joshua Holzworth
#######

import getopt
import sys

from parsing import parser
#import parser
import hdfs_utils

import shutil

#Pull LZ files from hdfs



#Parse csvs placed in LLZ

#Push parsed contents to TLZ

#Create metadata in TLZ

#Push all files found in TLZ to PZ



#Things needs to run
#batchID
#LZ
#PZ


#Pulls hdfs landingZone files onto the local file directory
def setupLLZ(landingZone, localLandingZone):
	parser.validateOutput(localLandingZone)
	hdfs_utils.getFiles(landingZone,localLandingZone)

#Parses all files found in localLandingZone
#Puts the parsed files (which are parsed by partition)
#Into the transitionZone which is located on local file system
def parseLLZ(batchID,transitionZone,localLandingZone,partitionCols):
	parser.parseCSVAndWrite(batchID,transitionZone,localLandingZone,{int(partitionCols)})

#Writes stored metadata from parsing to the transition zone
def writeMetadata(transitionZone,batchID):
	parser.writeMetadata(transitionZone,batchID)

#Pushes all files in transition zone to the partition zone
def pushToPZ(transitionZone,partitionZone):
	hdfs_utils.putFiles(transitionZone,partitionZone)

#Clean the passed in directories
#This means full deletion of parameter directory
def cleanup(directory):
	shutil.rmtree(directory)

def usage():
	print 'Usage'

def main():
	batchID = None
	landingZone = None
	transitionZone = None
	partitionZone = None
	partitionCols = None
	#Need to make sure this exists and create it if it doesn't
	localLandingZone = 'LLZ'

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hb:l:t:p:c:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-b", "--batchID"):
			batchID = arg
		elif opt in ("-l","--landingZone"):
			landingZone = arg
		elif opt in ("-t","--transitionZone"):
			transitionZone = arg
		elif opt in ("-p","--partitionZone"):
			partitionZone = arg
		elif opt in ("-c","--partitionCols"):
			partitionCols = arg

	if batchID is None or landingZone is None or partitionZone is None:
		usage()
		sys.exit(1)

	setupLLZ(landingZone,localLandingZone)
	parseLLZ(batchID,transitionZone,localLandingZone,partitionCols)
	writeMetadata(transitionZone,batchID)
	pushToPZ(transitionZone,partitionZone)
	cleanup(localLandingZone)
	cleanup(transitionZone)

if __name__ == "__main__":
	exit(main())