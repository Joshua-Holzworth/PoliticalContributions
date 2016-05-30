#!/usr/bin/env python3
import argparse
import sys

import src.python.utils as utils
import src.python.hdfs_utils as hdfs_utils
from src.python.hive import HqlRunner

LOGGING_NAME = 'dedup.py'
LOG_LOCATION = None
FAIL_MSG = 'Dedup failed!'

def main():
    args = parse_args()

    global LOGGING_NAME, LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    hdfs_utils.mkdir(args.output_table_data_directory)
    hdfs_utils.mkdir(args.ez_table_data_directory)

    if not hdfs_utils.dir_exists(args.fz_table_data_directory):
        utils.log('FZ data directory "' + fz_table_data_directory + '" does ' +
                  'not exist', LOGGING_NAME, utils.ERROR, LOG_LOCATION)
        sys.exit(1)

    hql = HqlRunner(args.parent_name, args.log_location, exit_on_fail=True)
    
    # Create EndZone table if not exists
    hql.run(args.ez_ddl_hql_path, fail_message=FAIL_MSG, db=args.db,
            table_name=args.ez_table, data_directory=args.ez_table_data_directory)
    # Create output table if not exists
    hql.run(args.output_ddl_hql_path, fail_message=FAIL_MSG, db=args.db,
            table_name=args.output_table, data_directory=args.output_table_data_directory)
    # Add partition if not exists to output table
    hql.run(args.add_partition_hql_path, fail_message=FAIL_MSG, db=args.db, 
            table_name=args.output_table, batch_id=args.batch_id)
    # Create FilteredZone table if not exists
    hql.run(args.fz_ddl_hql_path, fail_message=FAIL_MSG, db=args.db,
            table_name=args.fz_table, data_directory=args.fz_table_data_directory)
    # Add partition if not exists to FilteredZone table
    hql.run(args.add_partition_hql_path, fail_message=FAIL_MSG, db=args.db, 
            table_name=args.fz_table, batch_id=args.batch_id)

    # Run dedupe
    hql.run(args.dedup_hql_path, fail_message=FAIL_MSG, db=args.db, 
            fz_table=args.fz_table, ez_table=args.ez_table, 
            output_table=args.output_table, batch_id=batch_id)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-o', '--output-table', required=True)
    argparser.add_argument('-of', '--output-table-data-directory', required=True)
    argparser.add_argument('-fz', '--fz-table', required=True)
    argparser.add_argument('-fzf', '--fz-table-data-directory', required=True)
    argparser.add_argument('-ez', '--ez-table', required=True)
    argparser.add_argument('-ezf', '--ez-table-data-directory', required=True)
    argparser.add_argument('-ddlot', '--output-ddl-hql-path', required=True)
    argparser.add_argument('-ddlfz', '--fz-ddl-hql-path', required=True)
    argparser.add_argument('-ddlez', '--ez-ddl-hql-path', required=True)
    argparser.add_argument('-part', '--add-partition-hql-path', required=True)
    argparser.add_argument('--dedup-hql-path', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    return argparser.parse_args()

if __name__ == '__main__':
    exit(main())
