#!/usr/local/bin/python3 -B
import argparse
import src.python.utils as utils
import conf as pz_conf

def get_dedup_command(command_args):
    command = 'hive --hiveconf output_table=' + command_args.output_table
    command += ' --hiveconf pz_table=' + command_args.pz_table
    command += ' --hiveconf fz_table=' + command_args.fz_table
    command += ' --hiveconf pz_batch_min=' + command_args.pz_batch_min
    command += ' --hiveconf pz_batch_max=' + command_args.pz_batch_max
    return command

def get_expenditures_dedup_command(command_args):
    command = get_dedup_command(command_args)
    command += ' -f ' + pz_conf.expenditures_dedup_script_path
    return command

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output-table', required=True)
    argparser.add_argument('--pz-table', required=True)
    argparser.add_argument('--fz-table', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)

    args = argparser.parse_args()

    dedup_command = get_expenditures_dedup_command(args)

    utils.log("Expenditures dedup run")
    utils.log(dedup_command)
    exit_code, stdout, stderr = (utils.capture_command_output(dedup_command))

if __name__ == '__main__':
    main()
