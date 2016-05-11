#!/usr/bin/python3 -B
#######
##    Author: Joshua Holzworth
##
##    Pull LZ files from hdfs
##    
##    Parse csvs placed in LLZ
##    
##    Push parsed contents to TLZ
##    
##    Create metadata in TLZ
##    
##    Push all files found in TLZ to PZ
#######
import argparse

from parsing import parser
import hdfs_utils
import shutil

def main():
    batch_id, landing_zone, transition_zone, partition_zone, partition_cols = parse_args()
    #Need to make sure this exists and create it if it doesn't
    local_landing_zone = 'LLZ'

    setup_llz(landing_zone + '/batch_id=' + batch_id, local_landing_zone)
    parse_llz(batch_id, transition_zone, local_landing_zone, partition_cols)
    write_metadata(transition_zone, batch_id)
    push_to_pz(transition_zone, partition_zone)
    cleanup(local_landing_zone)
    cleanup(transition_zone)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-l', '--landing-zone', required=True)
    argparser.add_argument('-t', '--transition-zone', required=True)
    argparser.add_argument('-p', '--partition-zone', required=True)
    argparser.add_argument('-c', '--partition-cols', required=True)

    args = argparser.parse_args()

    return (args.batch_id, args.landing_zone, args.transition_zone,
            args.partition_zone, args.partition_cols)

#Pulls hdfs landing_zone files onto the local file directory
def setup_llz(landing_zone, local_landing_zone):
    parser.validate_output(local_landing_zone)
    hdfs_utils.get_files(landing_zone, local_landing_zone)

#Parses all files found in local_landing_zone
#Puts the parsed files (which are parsed by partition)
#Into the transition_zone which is located on local file system
def parse_llz(batch_id, transition_zone, local_landing_zone, partition_cols):
    parser.parse_csv(batch_id, transition_zone, local_landing_zone, {int(partition_cols)})

#Writes stored metadata from parsing to the transition zone
def write_metadata(transition_zone, batch_id):
    parser.write_metadata(transition_zone, batch_id)

#Pushes all files in transition zone to the partition zone
def push_to_pz(transition_zone, partition_zone):
    hdfs_utils.put_files(transition_zone, partition_zone)

#Clean the passed in directories
#This means full deletion of parameter directory
def cleanup(directory):
    shutil.rmtree(directory)

if __name__ == '__main__':
    exit(main())
