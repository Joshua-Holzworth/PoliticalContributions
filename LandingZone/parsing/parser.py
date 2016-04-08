#!/usr/bind/python
#
#####
##	Author Joshua Holzworth
#####

import os
import logging
import csv

metadataCount = {};
fileDictionary = {};

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
def parseCSV(batchID, outputDir, rootDir, partitionCols):
	validateOutput(outputDir)
	toParseFileNames = listDirectory(rootDir)
	print toParseFileNames
	for fileName in toParseFileNames:
		with open (rootDir + '/' + fileName) as fileConts:
			for line in fileConts:
				partition = parseLine(line, partitionCols)
				if partition not in metadataCount:
					metadataCount[partition] = 0
				metadataCount[partition] = metadataCount[partition] + 1
				if partition not in fileDictionary:
					fileDictionary[partition] = outputDir + '/' + partition + batchID + ".csv"
				outputFile = fileDictionary[partition]
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

	for result in csv.reader([line]):
		for partCol in partitionCols:
			partitionOutput = partitionOutput + result[partCol]
	partitionOutput = partitionOutput.replace(" ","")
	return partitionOutput











