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
    args = parse_args()

    dal = DataAccessLayer(Connector(args.hbase_connection), args.table)

    dal.increment_step(args.next_step)

    return_code = 0
    return return_code

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', '--next-step', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    return argparser.parse_args()

if __name__ == "__main__":
    exit(main())
