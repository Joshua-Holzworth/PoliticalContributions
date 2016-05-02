#!/usr/local/bin/python3 -B
import argparse

import src.python.ddl as ddl

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-e', 
                           '--expenditures-table-name', 
                           required=True)
    argparser.add_argument('-ef', 
                           '--expenditures-directory', 
                           required=True)
    argparser.add_argument('-c', 
                           '--contributions-table-name', 
                           required=True)
    argparser.add_argument('-cf', 
                           '--contributions-directory', 
                           required=True)

    args = argparser.parse_args()

    ddl.create_tables(command_args.contributions_table_name,
                      command_args.contributions_directory,
                      command_args.expenditures_directory,
                      command_args.expenditures_directory)

if __name__ == '__main__':
    main()
