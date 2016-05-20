#!/usr/bin/env python3
import argparse

import src.python.utils as utils
import src.python.hdfs_utils as hdfs_utils

LOGGING_NAME = 'contributions_dedup.py'
LOG_LOCATION = None

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-o', '--output-table', required=True)
    argparser.add_argument('-of', '--output-table-data-directory', required=True)
    argparser.add_argument('-pz', '--pz-table', required=True)
    argparser.add_argument('-fz', '--fz-table', required=True)
    argparser.add_argument('-fzf', '--fz-table-data-directory', required=True)
    argparser.add_argument('-ddl', '--data-ddl-hql-path', required=True)
    argparser.add_argument('--dedup-hql-path', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    global LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    hdfs_utils.mkdir(args.output_table_data_directory)
    hdfs_utils.mkdir(args.fz_table_data_directory)

    create_table(args.data_ddl_hql_path, args.db, args.output_table,
                 args.output_table_data_directory)
    create_table(args.data_ddl_hql_path, args.db, args.fz_table,
                 args.fz_table_data_directory)

    run_dedup(args.dedup_hql_path, args.db, args.pz_table, args.fz_table,
              args.output_table, args.pz_batch_min, args.pz_batch_max)

    return 0

def create_table(ddl_hql, db, table, table_dir):
    params = {
        'db': db,
        'table_name': table,
        'data_directory': table_dir
    }

    run_hive_file(ddl_hql, params)

def run_dedup(dedup_hql, db, pz_table, fz_table, output_table, pz_batch_min,
              pz_batch_max):
    params = {
        'output_table': output_table,
        'pz_table': pz_table,
        'fz_table': fz_table,
        'pz_batch_min': pz_batch_min,
        'pz_batch_max': pz_batch_max
    }

    run_hive_file(dedup_hql, params)
    
def run_hive_file(hql_path, parameters):
    hive_command = utils.build_hive_command(hql_path, parameters)
    utils.log('HiveCMD: ' + hive_command, LOGGING_NAME, utils.INFO,
              LOG_LOCATION)

    exit_code, stdout, stderr = utils.capture_command_output(hive_command)

    parse_hive_output(exit_code, stdout, stderr)

def parse_hive_output(exit_code, stdout, stderr):
    if exit_code:
        utils.log('Failure DEDUP FAILS!', LOGGING_NAME, utils.ERROR,
                  LOG_LOCATION)
        print(stdout)
        utils.print_stderr(stderr)
        exit(exit_code)

if __name__ == '__main__':
    exit(main())
