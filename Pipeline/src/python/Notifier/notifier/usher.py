#!/usr/bin/env python2.7
import argparse

from hbase.connector import Connector
from hbase.data_access_layer import DataAccessLayer

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--step', required=True)
    argparser.add_argument('-m', '--message',
                           help='Finished message or output', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    
    command_args = argparser.parse_args()

    connector = Connector(command_args.hbase_connection)
    dal = DataAccessLayer(connector, command_args.table)

    dal.set_step_to_finished(command_args.step, command_args.message)

if __name__ == '__main__':
    main()
