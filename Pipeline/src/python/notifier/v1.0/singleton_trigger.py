#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####
import argparse
import notifier_singleton

STATUS = 'Status'

def main():
	config_file_name, step_name, prev_step_name = parse_args()

	notifier_singleton.read_config(config_file_name)
	cur_status = notifier_singleton.step_running(step_name)

	#Defaults to -1
	prev_batch_id = -1

	if prev_step_name is not None:
		prev_status =  notifier_singleton.step_running(prev_step_name)
		prev_batch_id = int(notifier_singleton.get_batch_id(prev_step_name))
		if prev_status == "Running" or prev_status == "Stopped":
			prev_batch_id = prev_batch_id - 1

	triggered = True if cur_status == 'Stopped' or cur_status == 'Started' else False

	current_batch_id = int(notifier_singleton.get_batch_id(step_name))

	
	triggered = triggered and (True if current_batch_id <= prev_batch_id else False)
	
	if prev_status == "Running" or prev_status == "Stopped" and str(current_batch_id) == str(prev_batch_id):
		triggered = False

	if triggered:
		notifier_singleton.running_step(step_name)
		notifier_singleton.write_config(config_file_name)

	batch_id_json_blob =  "\"batchid\" : \"" + str(current_batch_id) + "\", \"batchIDMin\" : \"" + str(current_batch_id) + "\", \"batchIDMax\" : \"" + str(current_batch_id) + "\""

	jsonOutput = "{\"triggered\":" + ("true" if triggered else "false") + ", \"step\": \"" + step_name + "\", " + batch_id_json_blob + "}"
	print(jsonOutput)
	return 0

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config-file-name', required=True)
    argparser.add_argument('-s', '--step-name', required=True)
    argparser.add_argument('-p', '--prev-step-name', required=True)

    args = argparser.parse_args()

    return args.config_file_name, args.step_name, args.prev_step_name

if __name__ == "__main__":
	exit(main())
