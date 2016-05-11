#!/usr/bin/env python2.7
#######
##    Authors: Joshua Holzworth
##             Garrett Holbrook
#######
import os
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

def main():
    path, next_step, connection_string, table = parse_args()

    connector = Connector(connection_string)
    dal = DataAccessLayer(connector, table)

    dal.increment_step(next_step)

    return_code = 0
    return return_code

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

if __name__ == "__main__":
    exit(main())
