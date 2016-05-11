#!/usr/bin/env python2.7
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

def main():
    step, message, table, hbase_connection = parse_args()

    dal = DataAccessLayer(Connector(hbase_connection), table)
    dal.set_step_to_finished(step, message)

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
    
    args = argparser.parse_args()

    return args.step, args.message, args.table, args.hbase_connection

if __name__ == '__main__':
    main()
