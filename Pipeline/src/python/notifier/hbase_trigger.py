#!/usr/bin/env python2.7
import argparse

from src.python.hbase.connector import Connector
from src.python.hbase.data_access_layer import DataAccessLayer

def main():
    prev_step, step, message, table, hbase_connection = parse_args()

    dal = DataAccessLayer(Connector(hbase_connection), table)

    finished_prev_step_id = dal.get_latest_batch_id_with_condition(
        prev_step, 'current:status', 'Finished')
    current_step_id = dal.get_latest_batch_id(step)

    triggered = False
    if current_step_id > finished_prev_step_id:
        triggered = True
        dal.increment_step(step)
        dal.set_step_to_running(step, message)
        current_step_id = dal.get_latest_batch_id(step)

    print_json_response(triggered, current_step_id)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--prev-step', required=True)
    argparser.add_argument('-s', '--step', required=True)
    argparser.add_argument('-m', '--message',
                           help='Finished message or output', required=True)
    argparser.add_argument('-t', '--table', required=True)
    argparser.add_argument('-c', '--hbase-connection',
                           help='HBase connection string', required=True)
    
    args = argparser.parse_args()

    return (args.prev_step, args.step, args.message, args.table,
            args.hbase_connection)

def print_json_response(triggered, batch_id):
    json_output = ('{"triggered": ' + str(triggered).lower() +
                   ', "batchid": "' + batch_id + '"}') 
    print(json_output)

if __name__ == '__main__':
    main()
