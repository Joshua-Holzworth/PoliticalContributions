#!/usr/bin/env python2.7
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

LOGGING_NAME = 'hbase_trigger.py'

def main():
    args = parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    dal = DataAccessLayer(Connector(args.hbase_connection), args.table)

    finished_prev_step_id = dal.get_latest_batch_id_with_condition(
        args.prev_step, 'current:status', 'Finished')
    current_step_id = dal.get_latest_batch_id(args.step)

    triggered = False
    if current_step_id > finished_prev_step_id:
        triggered = True
        current_step_id = dal.get_next_batch_id(current_step_id)

    print_json_response(triggered, current_step_id)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--prev-step', required=True)
    argparser.add_argument('-s', '--step', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)
    
    return argparser.parse_args()

def print_json_response(triggered, batch_id):
    json_output = ('{"triggered": ' + str(triggered).lower() +
                   ', "batchid": "' + batch_id + '"}') 
    print(json_output)

if __name__ == '__main__':
    exit(main())
