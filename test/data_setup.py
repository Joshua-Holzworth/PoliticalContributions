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
    hdfs_mkdir(test_conf.lz_contributions_data_dir)
    hdfs_mkdir(test_conf.lz_expenditures_data_dir)
    hdfs_mkdir(test_conf.pz_contributions_data_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_expenditures_data_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_contributions_metadata_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_mkdir(test_conf.pz_expenditures_metadata_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_mkdir(test_conf.dz_contributions_dir)
    hdfs_mkdir(test_conf.dz_expenditures_dir)
    hdfs_mkdir(test_conf.fz_contributions_dir)
    hdfs_mkdir(test_conf.fz_expenditures_dir)

def put_data_into_hdfs():
    hdfs_copy_from_local(test_conf.contributions_landing_data_path, test_conf.lz_contributions_data_dir)
    hdfs_copy_from_local(test_conf.expenditures_landing_data_path, test_conf.lz_expenditures_data_dir)
    hdfs_copy_from_local(test_conf.contributions_partitioned_data_path, test_conf.pz_contributions_data_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_copy_from_local(test_conf.expenditures_partitioned_data_path, test_conf.pz_expenditures_data_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_copy_from_local(test_conf.contributions_result_data_path, test_conf.dz_contributions_dir)
    hdfs_copy_from_local(test_conf.expenditures_result_data_path, test_conf.dz_expenditures_dir)
    hdfs_copy_from_local(test_conf.contributions_result_data_path, test_conf.fz_contributions_dir)
    hdfs_copy_from_local(test_conf.expenditures_result_data_path, test_conf.fz_expenditures_dir)

def put_metadata_into_hdfs():
    hdfs_copy_from_local(test_conf.contributions_partitioned_metadata_path, test_conf.pz_contributions_metadata_dir + '/batch_id=' + test_conf.batch_id)
    hdfs_copy_from_local(test_conf.expenditures_partitioned_metadata_path, test_conf.pz_expenditures_metadata_dir + '/batch_id=' + test_conf.batch_id)

def main():
    create_hdfs_directories()
    put_data_into_hdfs()
    put_metadata_into_hdfs()

if __name__ == '__main__':
    main()
