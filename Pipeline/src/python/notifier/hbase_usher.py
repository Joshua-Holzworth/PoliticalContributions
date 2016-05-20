#!/usr/bin/env python2.7
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

LOGGING_NAME = 'hbase_usher.py'

def main():
    args = parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    dal = DataAccessLayer(Connector(args.hbase_connection), args.table)
    dal.set_step_to_finished(args.step, args.message)

    return_code = 0
    return return_code

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--step', required=True)
    argparser.add_argument('-m', '--message',
                           help='Finished message or output', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)
    
    return argparser.parse_args()

if __name__ == '__main__':
    exit(main())
