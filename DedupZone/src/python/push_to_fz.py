#!/usr/bin/python3 -B
import argparse

import src.python.utils as utils

LOGGING_NAME = 'push_to_fz.py'
PUSH_TO_FZ_HQL_PATH = utils.get_project_root_dir() + '/DedupZone/src/hive/push_to_fz.hql'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-fz', '--fz-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('-db', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    command = get_push_to_fz_command(args)

    utils.log('Pushing data from DZ to FZ with command: ' + command, 
               LOGGING_NAME, utils.INFO, args.log_location)
    exit_code, stdout, stderr = utils.capture_command_output(command)

    print(stdout)
    utils.print_stderr(stderr)

    return exit_code

def get_push_to_fz_command(command_args):
    return ('hive --hiveconf fz_table=' + command_args.fz_table_name +
               ' --hiveconf dz_table=' + command_args.dz_table_name +
               ' --hiveconf db=' + command_args.db +
               ' -f ' + PUSH_TO_FZ_HQL_PATH)

if __name__ == '__main__':
    main()
