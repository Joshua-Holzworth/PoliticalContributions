########
##    Author: Joshua Holzworth
########
import os

import src.python.utils as utils

HDFS_CMD = 'hdfs dfs'

#Obtain files on hdfs and place them on local
#  hdfs_dir - can also be referenced as src dir where files are located
#  local_dir - can also be refenced as dest dir where files will be pulled to
def get_files(hdfs_dir, local_dir):
    if os.path.exists(local_dir):
        pull_command = HDFS_CMD + ' -get ' + hdfs_dir + '/* ' + local_dir + '/.'

        utils.run_command(pull_command)

#Pushes all files locate din local_dir into hdfs_dir
def put_files(local_dir, hdfs_dir):
    if os.path.exists(local_dir):
        mkdir(hdfs_dir)
        push_command = HDFS_CMD + ' -put ' + local_dir + '/* ' + hdfs_dir + '/.'

        utils.run_command(push_command)

def mkdir(hdfs_dir):
    mkdir_command = HDFS_CMD + ' -mkdir -p ' + hdfs_dir
    utils.run_command(mkdir_command)

def rmdir(hdfs_dir):
    rmdir_command = HDFS_CMD + ' -rm -r ' + hdfs_dir
    utils.run_command(rmdir_command)

def dir_exists(hdfs_dir):
    check_command = HDFS_CMD + ' -test -d ' + hdfs_dir

    exit_code = utils.run_command(check_command)

    return True if exit_code == 0 else False

def file_exists(hdfs_file_path):
    check_command = HDFS_CMD + ' -test -f ' + hdfs_file_path

    exit_code = utils.run_command(check_command)

    return True if exit_code == 0 else False

def files_exist_in_dir(hdfs_dir):
    command = HDFS_CMD + ' -ls ' + hdfs_dir

    exit_code, stdout, stderr = utils.capture_command_output(command)

    return True if stdout else False
