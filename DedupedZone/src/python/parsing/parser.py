#!/usr/bin/python3 -B
#
#####
##    Author Joshua Holzworth
#####
import os
import csv

import src.python.utils as utils

metadata_count = {};
file_dictionary = {};

TOTAL_STR = 'TOTAL'
BASE_COUNT = 0
INCR_AMNT = 1
METADATA_FILE_NAME = 'metadata'
LOGGING_NAME = 'parsing/parser.py'

metadata_count[TOTAL_STR] = BASE_COUNT

#Recieve an output directory
#Read in each file from root Dir
#While reading each file write to a map that contains filename and row count
#Seeing as it must be csv right now then output the results into specific
#files in the output directory
#  batch_id - Current batch's respective ID that will be used to identify unique files
#  output_dir - The output directory where the partition files will be
#  root_dir - The directory where the previous files will be held
#  partition_cols - A list of numbers that specficies which columns are going to be partitioned on
#Function returns a map of metadata (Output File, Total Row Count)
def parse_csv(batch_id, output_dir, root_dir, partition_cols):
    validate_output(output_dir)
    to_parse_file_names = utils.list_directory(root_dir)

    for file_name in to_parse_file_names:
        with open (root_dir + '/' + file_name) as file_conts:
            for line in file_conts:
                partition = parse_line(line, partition_cols)
                
                update_metadata(partition, INCR_AMNT)

                output_file_dir = output_dir + '/data/batch_id=' + batch_id 
                validate_output(output_file_dir)
                output_file = output_file_dir + '/' + partition + '.csv'
                write_row(output_file, line)

#Validates output directory exists
#If it doesn't creates all directories need for the output dir to exist
#  output_dir - the output directory that will be checked / created
def validate_output(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

#Write a given row inside it's respective file
#  output_file_name - The output file where the respective row will be written to
#  line - The record value that is going to be written to the output file
#Doesn't return anything
def write_row(output_file_name, line):
    with open(output_file_name, 'a') as out_file:
        out_file.write(line)

#The line it recieves is expected to be a csv line
#Function overall consumes the line and partition columns
#It then returns a concatinated version of the partitions pulled from the line
#This results in a slight unique identifier (used for partitioning)
#  line - the line consumed or expected record from a raw file
#  partition_cols - A list of numbers that specficies which columns are going to be partitioned on
#Returns a combined string of all specfied partition columns
def parse_line(line, partition_cols):
    partition_output = ""

    for result in csv.reader([line]):
        for part_col in partition_cols:
            partition_output = partition_output + result[part_col]

    partition_output = partition_output.replace(" ","")
    return partition_output

#Obtains the file output directory for data and metadata files
#  base_output_root_dir - The base root where output dir will be
#  partition - Used to generate a unique and valid directory, kept in a dictionary for reuse
#Returns output directory for data and metadata
def get_file_output_directory(base_output_root_dir, partition):
    if partition not in file_dictionary:
        file_dictionary[partition] = base_output_root_dir + '/' + partition

    output_file = file_dictionary[partition]
    return output_file

#Updates metadata counts based on partition and count
#  partition - The partition that will be referenced in metadata and file name
#  count - The incremental amount metadata counts will be updated by
#Does not return anything
def update_metadata(partition, count):
    if partition not in metadata_count:
        metadata_count[partition] = BASE_COUNT

    metadata_count[partition] = metadata_count[partition] + count
    metadata_count[TOTAL_STR] = metadata_count[TOTAL_STR] + count

#Appends all metadata information to an output metadata file
#  output_dir - Base output directory where the metadata file will be placed
#  batch_id - The current batch_id for where the metadata will be placed
#Does not return anything and cleans up after itself
def write_metadata(output_dir, batch_id):
    file_output_dir = output_dir + '/metadata/batch_id=' + batch_id
    validate_output(file_output_dir)
    output_file = file_output_dir + '/' + METADATA_FILE_NAME + '.csv'

    with open(output_file , 'a') as metadata_file:
        for key in metadata_count:
            next_line = key + ',' + str(metadata_count[key]) + '\n'
            metadata_file.write(next_line)
