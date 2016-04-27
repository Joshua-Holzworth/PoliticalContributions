#!/usr/local/bin/python3 -B
import os

import test.py3.conf as test_conf

command = 'hadoop fs -rm -r ' + test_conf.test_data_root_dir
os.system(command)
