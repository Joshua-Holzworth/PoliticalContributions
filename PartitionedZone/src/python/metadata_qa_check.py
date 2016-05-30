#!/usr/bin/env python3
########
##    Author: Joshua Holzworth
########

# Essentially when this is called we need to do a few things

# Create tables around data inside partition_zone DB
# We need the data tables
# partition_zone_ddl.hql
# We also need the metadata table
# pz_metadata_ddl.hql

# Then we need to alter both tables to add the new batch_id partition_zone
# add_partition 2-3 times with valid arguments

# Then we need to run the Hive command and check if the vals are correct

import os
import re
import argparse

import src.python.utils as utils
from src.python.hive import HqlRunner

LOGGING_NAME = 'metadata_qa_check.py'
LOG_LOCATION = None
METADATA_TABLE = 'metadata'
ADD_PARTITION_HQL = utils.get_project_root_dir() + '/src/hive/add_partition.hql'
METADATA_DDL_HQL = utils.get_project_root_dir() + '/LandingZone/src/hive/pz_metadata_ddl.hql'
FAIL_MESSAGE = 'Partition QA check failed!'

def main():
    args = parse_args()

    global LOGGING_NAME, LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    batch_id = args.batch_id
    pz_hdfs_dir = args.hdfs_location
    data_ddl_hql = args.data_ddl_hql_path
    qa_hql = args.qa_hql_path
    db = args.db
    data_table = args.data_table
    metadata_location = pz_hdfs_dir + '/metadata/'
    data_location = pz_hdfs_dir + '/data/'

    hql = HqlRunner(args.parent_name, args.log_location, exit_on_fail=True,
                    fail_on_stdout=True)

    # Create metadata table if not exists
    hql.run(METADATA_DDL_HQL, fail_message=FAIL_MESSAGE, db=db,
            metadataLoc=metadata_location) 
    # Create data table if not exists
    hql.run(data_ddl_hql, fail_messae=FAIL_MESSAGE, db=db, table_name=data_table,
            data_directory=data_location)
    # Add batch_id partition to metadata if not exists
    hql.run(ADD_PARTITION_HQL, fail_message=FAIL_MESSAGE, batch_id=batch_id, db=db,
            table_name=METADATA_TABLE)
    # Add batch_id partition to data if not exists
    hql.run(ADD_PARTITION_HQL, fail_message=FAIL_MESSAGE, batch_id=batch_id, db=db,
            table_name=data_table)

    # Do QA check
    hql.run(qa_hql, fail_message=FAIL_MESSAGE, db=db, metadataTable=METADATA_TABLE,
            dataTable=data_table, batch_id=batch_id)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-l', '--hdfs-location', required=True)
    argparser.add_argument('-ddl', '--data-ddl-hql-path', required=True)
    argparser.add_argument('-qa', '--qa-hql-path', required=True)
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-t', '--data-table', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    return argparser.parse_args()

if __name__ == '__main__':
    exit(main())
