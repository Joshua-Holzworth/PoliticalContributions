#!/usr/bin/python3 -B
import argparse

import src.python.utils as utils
import conf as dz_conf

LOGGING_NAME = 'push_to_fz.py'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-fz', '--fz-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    command = get_push_to_fz_command(args)

    utils.log('Pushing data from DZ to FZ with command: ' + command, 
               LOGGING_NAME, utils.INFO, args.log_location)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def get_push_to_fz_command(command_args):
    return ('hive --hiveconf fz_table=' + command_args.fz_table_name +
               ' --hiveconf dz_table=' + command_args.dz_table_name +
               ' -f ' + dz_conf.push_to_fz_script_path)

if __name__ == '__main__':
    main()
