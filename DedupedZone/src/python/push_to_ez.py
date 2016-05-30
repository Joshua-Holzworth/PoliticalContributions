#!/usr/bin/env python3
import argparse

import src.python.utils as utils
import src.python.hive as hive

LOGGING_NAME = 'push_to_ez.py'

def main():
    args = parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    param_dict = dict(batch_id=args.batch_id, db=args.db, ez_table=args.ez_table,
                      dz_table=args.dz_table)
    command = hive.build_hive_command(args.push_to_ez_hql_path, param_dict)

    utils.log('Pushing data from DZ to EZ with command: ' + command, 
               LOGGING_NAME, utils.INFO, args.log_location)
    exit_code, stdout, stderr = utils.capture_command_output(command)

    print(stdout)
    utils.print_stderr(stderr)

    return exit_code

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-ez', '--ez-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('-hql', '--push-to-ez-hql-path', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    return argparser.parse_args()

if __name__ == '__main__':
    exit(main())
