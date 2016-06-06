#!/usr/bin/env python3
import argparse

import src.python.utils as utils
import src.python.hive as hive

LOGGING_NAME = 'dz_qa_check.py'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-fz', '--fz-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('-hql', '--qa-hql-path', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    param_dict = dict(fz_table=args.fz_table_name, dz_table=args.dz_table_name,
                      db=args.db, batch_id=args.batch_id)
    qa_check_command = hive.build_hive_command(args.qa_hql_path, param_dict)

    utils.log('QA check PZ -> DZ w/ command: ' + qa_check_command, LOGGING_NAME,
              utils.INFO, args.log_location)
    exit_code, stdout, stderr = utils.capture_command_output(qa_check_command)

    # stdout prints the result of the query, in this case it is the count
    if stdout.strip() == '0':
        utils.log('QA check passed', LOGGING_NAME,
              utils.INFO, args.log_location)
    else:
        exit_code = 1

    print(stdout)
    utils.print_stderr(stderr)

    return exit_code

if __name__ == '__main__':
    exit(main())
