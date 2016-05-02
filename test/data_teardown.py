#!/usr/bin/python3 -B
import src.python.utils as utils
import test.python.conf as test_conf

command = 'hadoop fs -rm -r ' + test_conf.hdfs_data_root_dir
utils.run_command(command)
