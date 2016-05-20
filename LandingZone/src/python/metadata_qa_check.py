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

LOGGING_NAME = 'metadata_qa_check.py'
LOG_LOCATION = None
METADATA_TABLE = 'metadata'
ADD_PARTITION_HQL = utils.get_project_root_dir() + '/src/hive/add_partition.hql'
METADATA_DDL_HQL = utils.get_project_root_dir() + '/LandingZone/src/hive/pz_metadata_ddl.hql'

def main():
    args = parse_args()

    global LOGGING_NAME
    global LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    batch_id = args.batch_id
    pz_hdfs_dir = args.hdfs_location
    data_ddl_hql = args.data_ddl_hql_path
    qa_hql = args.qa_hql_path
    db = args.db
    data_table = args.data_table

    create_metadata_table(db, pz_hdfs_dir)
    create_data_table(data_ddl_hql, db, data_table, pz_hdfs_dir)

    add_metadata_partition(batch_id, db)
    add_data_partition(batch_id, db, data_table)
    
    do_qa_check(qa_hql, batch_id, db, data_table)

    return 0

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

def create_metadata_table(db, pz_hdfs_dir):
    metadata_ddl_params = {
        'db': db,
        'metadataLoc': pz_hdfs_dir + '/metadata/'
    }

    run_hive_file(METADATA_DDL_HQL, metadata_ddl_params)

def create_data_table(data_ddl_hql, db, data_table, pz_hdfs_dir):
    data_ddl_params = {
        'db': db,
        'table_name': data_table,
        'data_directory': pz_hdfs_dir + '/data/'
    }

    run_hive_file(data_ddl_hql, data_ddl_params)

def add_metadata_partition(batch_id, db): 
    params = {
        'db': db,
        'table_name': METADATA_TABLE,
        'batch_id': batch_id
    }

    run_hive_file(ADD_PARTITION_HQL, params)

def add_data_partition(batch_id, db, data_table): 
    params = {
        'db': db,
        'table_name': data_table,
        'batch_id': batch_id
    }

    run_hive_file(ADD_PARTITION_HQL, params)

def do_qa_check(qa_hql, batch_id, db, data_table):
    params = {
        'db': db,
        'metadataTable': METADATA_TABLE,
        'dataTable': data_table,
        'batch_id': batch_id
    }

    run_hive_file(qa_hql, params)

def run_hive_file(hql_path, parameters):
    hive_command = utils.build_hive_command(hql_path, parameters)
    utils.log('HiveCMD: ' + hive_command, LOGGING_NAME, utils.INFO,
              LOG_LOCATION)

    exit_code, stdout, stderr = utils.capture_command_output(hive_command)

    parse_hive_output(exit_code, stdout, stderr)

def parse_hive_output(exit_code, stdout, stderr):
    stdout = stdout.replace('\r', '')

    if stdout or exit_code:
        utils.log('Failure QA CHECK FAILS!', LOGGING_NAME, utils.ERROR,
                  LOG_LOCATION)
        print(stdout)
        utils.print_stderr(stderr)
        exit(exit_code)

if __name__ == '__main__':
    exit(main())
