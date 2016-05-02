#!/usr/bin/python3 -B

########
##	Author: Joshua Holzworth
########

#Essentially when this is called we need to do a few things

#Create tables around data inside partition_zone DB
#We need the data tables
#partition_zone_ddl.hql
#We also need the metadata table
#pz_metadata_ddl.hql

#Then we need to alter both tables to add the new batchID partition_zone
#add_partition 2-3 times with valid arguments


#Then we need to run the Hive command and check if the vals are correct

#pz_qa_check.hql

import getopt
import sys
import os
import subprocess
import re

def runHiveFile(hiveFile, parameters):
	hiveCmd = "hive -f " + hiveFile + " "+parameters
	hiveProc = subprocess.Popen(hiveCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	#hiveProc.stderr
	output,error = hiveProc.communicate()
	#print str(output)
	return str(output)


def usage():
	print('qa_check.py -b {BatchID} -l {baseHDFSlocation} ')

def parseHiveOutput(output):
	output = output.replace('\r','')
	if output == "":
		print("Success QA Check passes")
	else:
		print("Failure QA CHECK FAILS!")
		#Should examine what sections fail and print those out
		exit(414)

def main():
	#Takes in at least
	#A batchID
	#contributionsHDFS LOC
	#expendentituresHDFS LOC

	batchID = None
	baseHDFSLocation = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hb:l:")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ("-b", "--batchID"):
			batchID = arg
		elif opt in ("-l", "--hdfsLocation"):
			baseHDFSLocation = arg
		
	if batchID is None or baseHDFSLocation is None :
		usage()
		sys.exit(1)



	hiveDir = "hive/"
	pz_hql = hiveDir + "partition_zone_ddl.hql"
	pz_params = "--hiveconf conLoc=" + baseHDFSLocation + "/data/" 
	metadata_hql = hiveDir + "pz_metadata_ddl.hql"
	metadata_params = "--hiveconf metadataLoc="+baseHDFSLocation+"/metadata/"
	partition_hql = hiveDir + "add_partition.hql"

	#runHiveFile(metadata_hql,metadata_params)
	#runHiveFile(pz_hql,pz_params)

	#THIS SET OF 4 LINES NEEDS TO BE REFACTORED AT ANOTHER TIME
	#WE NEED THIS TO BE DYNAMIC -- This'll take a lot of time where there are other tasks to be done
	#For now this works and we'll get back to this when the time comes / backlog it
	#Honestly this entire script needs refactoring 
	partition1_args = "--hiveconf db_name=partition_zone --hiveconf table_name=metadata --hiveconf batch_id="+batchID
	#runHiveFile(partition_hql,partition1_args)
	
	partition2_args = "--hiveconf db_name=partition_zone --hiveconf table_name=contributions --hiveconf batch_id="+batchID
	#runHiveFile(partition_hql,partition2_args)
	
	qa_hql = hiveDir+"/pz_qa_check.hql"
	qa_params = "--hiveconf table_name=contributions"
	parseHiveOutput(runHiveFile(qa_hql,qa_params))


if __name__ == "__main__":
	exit(main())

