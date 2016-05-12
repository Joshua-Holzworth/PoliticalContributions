#!/usr/local/bin/python3 -B
import argparse

import src.python.utils as utils
import src.python.ddl as ddl
import conf as pz_conf

LOGGING_NAME = 'contributions_dedup.py'

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-o', '--output-table', required=True)
    argparser.add_argument('-of', '--output-table-data-directory', required=True)
    argparser.add_argument('-pz', '--pz-table', required=True)
    argparser.add_argument('-fz', '--fz-table', required=True)
    argparser.add_argument('-fzf', '--fz-table-data-directory', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    global LOGGING_NAME
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME

    create_tables(args)

    dedup_command = get_contributions_dedup_command(args)
    utils.log('Running contributions dedup with command: ' + dedup_command,
              LOGGING_NAME, utils.INFO, args.log_location)

    exit_code, stdout, stderr = (utils.capture_command_output(dedup_command))
    
    print(stdout)
    utils.print_stderr(stderr)
    return exit_code

def create_tables(command_args):
    ddl.create_contributions_table(command_args.output_table,
                                   command_args.output_table_data_directory)
    ddl.create_contributions_table(command_args.fz_table,
                                   command_args.fz_table_data_directory)

def get_dedup_command(command_args):
    command = 'hive --hiveconf output_table=' + command_args.output_table
    command += ' --hiveconf pz_table=' + command_args.pz_table
    command += ' --hiveconf fz_table=' + command_args.fz_table
    command += ' --hiveconf pz_batch_min=' + command_args.pz_batch_min
    command += ' --hiveconf pz_batch_max=' + command_args.pz_batch_max
    return command

def get_contributions_dedup_command(command_args):
    command = get_dedup_command(command_args)
    command += ' -f ' + pz_conf.contributions_dedup_script_path
    return command

if __name__ == '__main__':
    main()
