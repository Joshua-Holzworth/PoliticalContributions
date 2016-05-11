#!/usr/bin/python3 -B

########
##    Author: Joshua Holzworth
########

#Essentially when this is called we need to do a few things

#Create tables around data inside partition_zone DB
#We need the data tables
#partition_zone_ddl.hql
#We also need the metadata table
#pz_metadata_ddl.hql

#Then we need to alter both tables to add the new batch_id partition_zone
#add_partition 2-3 times with valid arguments


#Then we need to run the Hive command and check if the vals are correct

import os
import re
import argparse

import src.python.utils as utils

LOGGING_NAME = 'LandingZone/qa_check.py'

batch_id = None

def main():
    global batch_id
    batch_id, base_hdfs_location = parse_args()

    hive_dir = "hive/"
    pz_hql = hive_dir + "partition_zone_ddl.hql"
    pz_params = "--hiveconf conLoc=" + base_hdfs_location + "/data/" 
    metadata_hql = hive_dir + "pz_metadata_ddl.hql"
    metadata_params = "--hiveconf metadataLoc=" + base_hdfs_location + "/metadata/"
    partition_hql = hive_dir + "add_partition.hql"

    run_hive_file(metadata_hql, metadata_params)
    run_hive_file(pz_hql, pz_params)

    #THIS SET OF 4 LINES NEEDS TO BE REFACTORED AT ANOTHER TIME
    #WE NEED THIS TO BE DYNAMIC -- This'll take a lot of time where there are other tasks to be done
    #For now this works and we'll get back to this when the time comes / backlog it
    #Honestly this entire script needs refactoring 
    partition1_args = "--hiveconf db_name=partition_zone --hiveconf table_name=metadata --hiveconf batch_id="+batch_id
    run_hive_file(partition_hql, partition1_args)
    
    partition2_args = "--hiveconf db_name=partition_zone --hiveconf table_name=contributions --hiveconf batch_id="+batch_id
    run_hive_file(partition_hql, partition2_args)
    
    qa_hql = hive_dir + "pz_qa_check.hql"
    qa_params = "--hiveconf table_name=contributions"

    stdout, stderr = run_hive_file(qa_hql, qa_params)
    parse_hive_output(stdout, stderr)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-l', '--hdfs-location', required=True)

    command_args = argparser.parse_args()

    return command_args.batch_id, command_args.hdfs_location

def run_hive_file(hiveFile, parameters):
    root_dir = utils.get_project_root_dir() + '/LandingZone/src/'
    hive_command = "hive -f " + root_dir + hiveFile + " " + parameters

    utils.log("HiveCMD: " + hive_command, level=utils.INFO, name=LOGGING_NAME)

    exit_code, stdout, stderr = utils.capture_command_output(hive_command)
    return stdout, stderr

def parse_hive_output(stdout, stderr):
    stdout = stdout.replace('\r', '')

    if stdout == '' and stderr == '':
        utils.log("Success QA Check passes", level=utils.INFO, name=LOGGING_NAME)
    else:
        utils.log("Failure QA CHECK FAILS!", level=utils.ERROR, name=LOGGING_NAME)
        #Should examine what sections fail and print those out
        exit(414)

if __name__ == "__main__":
    exit(main())

