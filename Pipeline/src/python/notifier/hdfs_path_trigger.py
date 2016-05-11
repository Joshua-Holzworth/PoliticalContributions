#!/usr/bin/env python2.7
#######
##    Authors: Joshua Holzworth
##             Garrett Holbrook
#######
import os
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

import src.python.hdfs_utils as hdfs_utils

schema = {
    'current': dict(),
    'attemptStart': dict(),
    'attemptEnd': dict()
}

def main():
    path, next_step, connection_string, table = parse_args()

    connector = Connector(connection_string)
    dal = DataAccessLayer(connector, table)

    dal.create_table_if_not_exists(schema)
    next_batch_id = dal.get_latest_batch_id(next_step) - 1

    new_batch_exists = hdfs_utils.dir_exists(path + '/batch_id=' + str(next_batch_id))
    rc = (0 if new_batch_exists else 1)

    print_json_response(new_batch_exists)
    return rc

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--path', help='HDFS directory to check',
                           required=True)
    argparser.add_argument('-n', '--next-step', require=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)

    args = argparser.parse_args()

    return args.file, args.next_step, args.hbase_connection, args.table

def print_json_response(new_batch_exists):
    json_output = ('{"triggered":' + 
                  str(new_batch_exists).lower() + 
                  ', "Parameter1":"override!"}')
    print(json_output)

if __name__ == "__main__":
    exit(main())
