#!/usr/local/bin/python3 -B
import argparse
import src.py3.utils as utils
import conf as dz_conf

def get_dedup_command(command_args):
    command = 'hive --hiveconf output_table=' + command_args.output_table
    command += ' --hiveconf pz_table=' + command_args.pz_table
    command += ' --hiveconf fz_table=' + command_args.fz_table
    command += ' --hiveconf pz_batch_min=' + command_args.pz_batch_min
    command += ' --hiveconf pz_batch_max=' + command_args.pz_batch_max
    return command

def get_contributions_dedup_command(command_args):
    command = get_dedup_command(command_args)
    command += ' -f ' + dz_conf.contributions_dedup_script_path
    return command

def get_expenditures_dedup_command(command_args):
    command = get_dedup_command(command_args)
    command += ' -f ' + dz_conf.expenditures_dedup_script_path
    return command

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output-table', required=True)
    argparser.add_argument('--pz-table', required=True)
    argparser.add_argument('--fz-table', required=True)
    argparser.add_argument('--pz-batch-min', required=True)
    argparser.add_argument('--pz-batch-max', required=True)

    args = argparser.parse_args()

    contributions_dedup_command = get_contributions_dedup_command(args)
    expenditures_dedup_command = get_expenditures_dedup_command(args)

    utils.log("Contributions dedup run")
    contributions_exit_code, contributions_stdout, contributions_stderr = (
        utils.capture_command_output(contributions_dedup_command))
    utils.log("\nExpenditures dedup run")
    expenditures_exit_code, expenditures_stdout, expenditures_stderr = (
        utils.capture_command_output(expenditures_dedup_command))

if __name__ == '__main__':
    main()
