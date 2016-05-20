#!/usr/bin/env python
#####
##    Author: Joshua Holzworth
#####
import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

import notifier_singleton
    
def main():
    config_file_name, current_step, return_code, next_step = parse_args()

    notifier_singleton.read_config(config_file_name)

    if notifier_singleton.step_running(current_step) == "Running":
        if return_code == "1":
            notifier_singleton.stop_event(current_step)
        elif return_code == "0":
            current_batch_id = notifier_singleton.get_batch_id(current_step)

            if next_step != None:
                next_step_status = notifier_singleton.step_running(next_step)
                if next_step_status == 'Finished':
                    next_step_batch_id = notifier_singleton.get_batch_id(next_step)
                    if next_step_batch_id < current_batch_id:
                        notifier_singleton.increment_batch_id(next_step)
                        notifier_singleton.start_step(next_step)

            notifier_singleton.finish_event(current_step)

        notifier_singleton.write_config(config_file_name)
    else:
        print('Nothing to usher')

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-s', '--current-step', required=True)
    argparser.add_argument('-r', '--return-code', required=True)
    argparser.add_argument('-n', '--next-step', required=True)

    args = argparser.parse_args()

    return args.config_file_name, args.current_step, args.return_code, args.next_step

if __name__ == "__main__":
    exit(main())
