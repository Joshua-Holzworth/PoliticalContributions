########
##    Author: Joshua Holzworth
########
import os

import src.python.utils as utils

HDFS_CMD = 'hdfs dfs'
LOGGING_NAME = 'hdfs_utils.py'

#Obtain files on hdfs and place them on local
#  hdfs_dir - can also be referenced as src dir where files are located
#  local_dir - can also be refenced as dest dir where files will be pulled to
def get_files(hdfs_dir, local_dir):
    if os.path.exists(local_dir):
        pull_command = HDFS_CMD + ' -get ' + hdfs_dir + '/* ' + local_dir + '/.'

        utils.log('Pulling files with command ' + pull_command,
                  level=utils.INFO, name=LOGGING_NAME)

        utils.run_command(pull_command)
    else:
        utils.log(local_dir + ' does not exist', 
                  level=utils.ERROR, name=LOGGING_NAME)

#Pushes all files locate din local_dir into hdfs_dir
def put_files(local_dir, hdfs_dir):
    if os.path.exists(local_dir):
        push_command = HDFS_CMD + ' -put ' + local_dir + '/* ' + hdfs_dir + '/.'

        utils.log('Pushing files with command ' + push_command,
                  level=utils.INFO, name=LOGGING_NAME)
        utils.run_command(push_command)
    else:
        utils.log(local_dir + ' does not exists',
                  level=utils.ERROR, name=LOGGING_NAME)
