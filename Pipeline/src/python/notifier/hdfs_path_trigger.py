#!/usr/bin/env python2.7
#######
##    Authors: Joshua Holzworth
##             Garrett Holbrook
#######
import os
import argparse

import src.python.utils as utils
import src.python.hdfs_utils as hdfs_utils
from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

LOGGING_NAME = 'hdfs_path_trigger.py'
SCHEMA = {
    'current': dict(),
    'attemptStart': dict(),
    'attemptEnd': dict()
}

def main():
    args = parse_args()

    global LOGGING_NAME
    global LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    path = args.path
    next_step = args.next_step
    connection_string = args.hbase_connection
    table = args.table

    connector = Connector(connection_string)
    dal = DataAccessLayer(connector, table)

    dal.create_table_if_not_exists(SCHEMA)
    next_batch_id = dal.get_next_batch_id(dal.get_latest_batch_id(next_step))

    path_to_check = path + '/batch_id=' + str(next_batch_id)
    utils.log('Checking hdfs path "' + path_to_check + '"', LOGGING_NAME,
              utils.INFO, LOG_LOCATION)
    new_batch_exists = hdfs_utils.files_exists_in_dir(path_to_check)
    rc = (0 if new_batch_exists else 1)

    print_json_response(new_batch_exists)
    return rc

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--path', help='HDFS directory to check',
                           required=True)
    argparser.add_argument('-n', '--next-step', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    return argparser.parse_args()

def print_json_response(new_batch_exists):
    json_output = ('{"triggered": "' + 
                  str(new_batch_exists).lower() + '"}')
    print(json_output)

if __name__ == "__main__":
    exit(main())
