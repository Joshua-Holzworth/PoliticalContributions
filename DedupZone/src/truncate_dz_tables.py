#!/usr/local/bin/python3 -B
import argparse
import src.py3.utils as utils
import src.py3.conf as conf

def get_create_table_command(command_args):
    command = (
        "hive -e 'TRUNCATE TABLE " + 
        command_args.expenditures_table_name +
        "; TRUNCATE TABLE " + command_args.contributions_table_name + ";'"
        )
    return command

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-e', 
                           '--expenditures-table-name', 
                           required=True)
    argparser.add_argument('-c', 
                           '--contributions-table-name', 
                           required=True)

    args = argparser.parse_args()

    command = get_create_table_command(args)

    utils.log("Removing data from dz tables")
    utils.log(command)
    exit_code, stdout, stderr = utils.run_command(command)

if __name__ == '__main__':
    main()
