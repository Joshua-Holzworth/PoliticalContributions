#!/usr/bin/python3 -B
import argparse

import src.python.utils as utils
import test.python.conf as test_conf
import test.python.utils as test_utils

def hdfs_mkdir(path):
    command = 'hadoop fs -mkdir -p ' + path
    utils.log(command)
    utils.run_command(command)

def hdfs_copy_from_local(local_path, destination_path):
    command = 'hadoop fs -copyFromLocal ' + local_path + ' ' + destination_path
    utils.log(command)
    utils.run_command(command)

def create_hdfs_directories():
    hdfs_mkdir(test_conf.lz_contributions_data_dir + '/' + test_conf.batch_id)
    hdfs_mkdir(test_conf.lz_expenditures_data_dir + '/' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_contributions_data_dir + '/' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_expenditures_data_dir + '/' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_contributions_metadata_dir + '/' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_expenditures_metadata_dir + '/' + test_conf.batch_id)

def put_test_data_into_hdfs(contributions_path, expenditures_path):
    hdfs_copy_from_local(contributions_path, test_conf.lz_contributions_data_dir + '/' + test_conf.batch_id)
    hdfs_copy_from_local(expenditures_path, test_conf.lz_expenditures_data_dir + '/' + test_conf.batch_id)
    hdfs_copy_from_local(contributions_path, test_conf.pz_contributions_data_dir + '/' + test_conf.batch_id)
    hdfs_copy_from_local(expenditures_path, test_conf.pz_expenditures_data_dir + '/' + test_conf.batch_id)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--contributions-path', help='Local path to contributions data', required=True)
    argparser.add_argument('-e', '--expenditures-path', help='Local path to contributions data', required=True)

    args = argparser.parse_args()
    
    create_hdfs_directories()
    put_test_data_into_hdfs(args.contributions_path, args.expenditures_path)

if __name__ == '__main__':
    main()
