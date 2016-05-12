#!/usr/bin/env python2.7
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

def main():
    step, table, hbase_connection = parse_args()

    dal = DataAccessLayer(Connector(hbase_connection), table)

    row_key, current_step = dal.get_latest_step_batch(step)
    batch_id = dal.get_batch_id_from_row_key(row_key)

    triggered = False
    if current_step['current:status'] == 'Started':
        triggered = True
        dal.set_step_to_running(step, 'Found status of "Started" for ' +
                                      'batch_id ' + str(batch_id))

    print_json_response(triggered, batch_id)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--step', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    
    args = argparser.parse_args()

    return args.step, args.table, args.hbase_connection

def print_json_response(triggered, batch_id):
    json_output = ('{"triggered": ' + str(triggered).lower() + 
                   ', "batchid": ' + batch_id + '}') 
    print(json_output)

if __name__ == '__main__':
    main()
