#!/usr/bin/python3 -B
import argparse

import src.python.utils as utils
import conf as dz_conf

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-pz', '--pz-table-name', required=True)
    argparser.add_argument('-dz', '--dz-table-name', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)

    command_args = argparser.parse_args()

    qa_check_command = get_qa_check_command(command_args)

    utils.log('QA check PZ -> DZ')
    utils.log(qa_check_command)
    exit_code, stdout, stderr = utils.capture_command_output(qa_check_command)

    # stdout prints the result of the query, in this case it is the count
    if stdout.strip() == '0':
        utils.log('QA check passed')
    else:
        utils.log('QA check failed!')
        utils.log('EXIT CODE: ' + str(exit_code))
        utils.log('STDOUT: ' + stdout)
        utils.log('STDERR: ' + stderr)

def get_qa_check_command(command_args):
    command = 'hive --hiveconf pz_table=' + command_args.pz_table_name
    command += ' --hiveconf dz_table=' + command_args.dz_table_name
    command += ' --hiveconf pz_batch_min=' + command_args.pz_batch_min
    command += ' --hiveconf pz_batch_max=' + command_args.pz_batch_max
    command += ' -f ' + dz_conf.qa_check_script_path

    return command

if __name__ == '__main__':
    main()
