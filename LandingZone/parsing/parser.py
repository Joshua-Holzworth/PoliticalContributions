#!/usr/bin/python
#
#####
##	Author Joshua Holzworth
#####

import os
import logging
import csv

metadataCount = {};
fileDictionary = {};

TOTAL_STR = 'TOTAL'
BASE_COUNT = 0
INCR_AMNT = 1
METADATA_FILE_NAME = 'metadata'

#s
metadataCount[TOTAL_STR] = BASE_COUNT

#Recieve an output directory
#Read in each file from root Dir
#While reading each file write to a map that contains filename and row count
#Seeing as it must be csv right now then output the results into specific
#files in the output directory
#  batchID - Current batch's respective ID that will be used to identify unique files
#  outputDir - The output directory where the partition files will be
#  rootDir - The directory where the previous files will be held
#  partitionCols - A list of numbers that specficies which columns are going to be partitioned on
#Function returns a map of metadata (Output File, Total Row Count)
def parseCSVAndWrite(batchID, outputDir, rootDir, partitionCols):
	validateOutput(outputDir)
	toParseFileNames = listDirectory(rootDir)
	print toParseFileNames
	for fileName in toParseFileNames:
		with open (rootDir + '/' + fileName) as fileConts:
			for line in fileConts:
				partition = parseLine(line, partitionCols)
				
				updateMetadata(partition,INCR_AMNT)

				outputFileDir = getFileOutputDirectory(outputDir + 'data/' + batchID , partition)
				validateOutput(outputFileDir)
				outputFile = outputFileDir + '/' + batchID + '.csv'
				writeRow(outputFile,line)


#Validates output directory exists
#If it doesn't creates all directories need for the output dir to exist
#  outputDir - the output directory that will be checked / created
def validateOutput(outputDir):
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

#Write a given row inside it's respective file
#  outputFileName - The output file where the respective row will be written to
#  line - The record value that is going to be written to the output file
#Doesn't return anything
def writeRow(outputFileName, line):
	with open(outputFileName,'a') as outFile:
		outFile.write(line)

#Lists all files found in a directory
#This isn't recursive currently
#  rootDir - The directory that will be used to read files from
#Function returns a collection of file names
def listDirectory(rootDir):
	validDir = os.path.isdir(rootDir)
	if validDir == False:
		logging.error("Directory: " + rootDir + " is not a valid directory.")
	else:
		files = os.listdir(rootDir)
	return files


#The line it recieves is expected to be a csv line
#Function overall consumes the line and partition columns
#It then returns a concatinated version of the partitions pulled from the line
#This results in a slight unique identifier (used for partitioning)
#  line - the line consumed or expected record from a raw file
#  partitionCols - A list of numbers that specficies which columns are going to be partitioned on
#Returns a combined string of all specfied partition columns
def parseLine(line, partitionCols):
	partitionOutput = ""

	for result in csv.reader([line],quotechar="\""):
		for partCol in partitionCols:
			partitionOutput = partitionOutput + result[partCol]
	partitionOutput = partitionOutput.replace(" ","")
	return partitionOutput


#Obtains the file output directory for data and metadata files
#  baseOutputRootDir - The base root where output dir will be
#  partition - Used to generate a unique and valid directory, kept in a dictionary for reuse
#Returns output directory for data and metadata
def getFileOutputDirectory(baseOutputRootDir, partition):
	if partition not in fileDictionary:
		fileDictionary[partition] = baseOutputRootDir + '/' + partition
	outputFile = fileDictionary[partition]
	return outputFile


#Updates metadata counts based on partition and count
#  partition - The partition that will be referenced in metadata and file name
#  count - The incremental amount metadata counts will be updated by
#Does not return anything
def updateMetadata(partition, count):
	if partition not in metadataCount:
		metadataCount[partition] = BASE_COUNT
	metadataCount[partition] = metadataCount[partition] + count
	metadataCount[TOTAL_STR] = metadataCount[TOTAL_STR] + count


#Appends all metadata information to an output metadata file
#  outputDir - Base output directory where the metadata file will be placed
#  batchID - The current batchID for where the metadata will be placed
#Does not return anything and cleans up after itself
def writeMetadata(outputDir, batchID):
	fileOutputDir = outputDir + '/metadata'
	validateOutput(fileOutputDir)
	fileOutputDir = fileOutputDir + '/' + batchID
	outputFile = fileOutputDir + METADATA_FILE_NAME + '.csv'
	with open(outputFile , 'a') as metadataFile:
		for key in metadataCount:
			nextLine = key + ',' + str(metadataCount[key]) + '\n'
			logging.info('Counts: ' + nextLine)
			metadataFile.write(nextLine)

