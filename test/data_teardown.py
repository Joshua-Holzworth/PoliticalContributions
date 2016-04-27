#!/usr/local/bin/python3 -B
import src.py3.utils as utils
import test.py3.conf as test_conf

command = 'hadoop fs -rm -r ' + test_conf.test_data_root_dir
utils.run_command(command)
