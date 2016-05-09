#!/usr/bin/env python2.7
#######
##    Authors: Joshua Holzworth
##             Garrett Holbrook
#######
import os
import argparse

from hbase.connector import Connector
from hbase.data_access_layer import DataAccessLayer

schema = {
    'current': dict(),
    'attemptStart': dict(),
    'attemptEnd': dict()
}

def main():
    file_path, connection_string, table = parse_args()

    file_exists = os.path.exists(file_path)
    rc = (0 if file_exists else 1)

    if file_exists:
        trigger(connection_string, table, file_path)

    print_json_response(file_exists)
    return rc

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--file', help='File to watch', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)

    command_args = argparser.parse_args()

    return command_args.file, command_args.hbase_connection, command_args.table

def print_json_response(file_exists):
    jsonOutput = ('{"triggered":' + 
                  str(file_exists).lower() + 
                  ', "Parameter1":"override!"}')
    print(jsonOutput)

def trigger(connection_string, table, file_path):
    connector = Connector(connection_string)
    dal = DataAccessLayer(connector, table)

    dal.create_table_if_not_exists(schema)
    dal.increment_step('test')
    dal.set_step_to_running('test', 'File found at ' + file_path)

if __name__ == "__main__":
    exit(main())
