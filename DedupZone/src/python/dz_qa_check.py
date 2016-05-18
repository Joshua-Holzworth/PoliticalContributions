#!/usr/bin/env python3
import argparse

import src.python.utils as utils

LOGGING_NAME = 'dz_qa_check.py'
QA_HQL_PATH = utils.get_project_root_dir() + '/DedupZone/src/hive/qa_check.hql'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-pz', '--pz-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('-db', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    qa_check_command = get_qa_check_command(args)

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

def get_qa_check_command(command_args):
    command = 'hive --hiveconf pz_table=' + command_args.pz_table_name
    command += ' --hiveconf dz_table=' + command_args.dz_table_name
    command += ' --hiveconf db=' + command_args.db
    command += ' --hiveconf pz_batch_min=' + command_args.pz_batch_min
    command += ' --hiveconf pz_batch_max=' + command_args.pz_batch_max
    command += ' -f ' + QA_HQL_PATH

    return command

if __name__ == '__main__':
    exit(main())
