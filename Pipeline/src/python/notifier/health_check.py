#!/usr/bin/python3 -B
#######
##    Author: Joshua Holzworth
#######
import argparse

import src.python.utils as utils

APP_SCRIPT_NAME = 'notifier.py'

def main():
    batch_id = parse_args()
    pid = -1

    process_list_command = 'ps aux | grep python | grep [n]otifier | grep ' + batch_id 

    exit_code, stdout, stderr = utils.capture_command_output(process_list_command)

    sections = stdout.split()

    if len(out):
        pid = sections[1]

    print(pid)

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)

   return argparser.parse_args().batch_id
    
if __name__ == '__main__':
    exit(main())
