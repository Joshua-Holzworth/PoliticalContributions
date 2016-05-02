#!/usr/bin/python3 -B
import argparse

import src.python.utils as utils
import src.python.ddl as ddl
import test.python.conf as test_conf
import test.python.utils as test_utils

def main():
    create_hdfs_directories()
    put_data_into_hdfs()
    put_metadata_into_hdfs()
    create_tables()
    add_partitions()

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

def create_tables():
    ddl.create_partitioned_tables(test_conf.pz_contributions_table,
                                  test_conf.pz_contributions_data_dir,
                                  test_conf.pz_expenditures_table,
                                  test_conf.pz_expenditures_data_dir)
    ddl.create_tables(test_conf.dz_contributions_table,
                      test_conf.dz_contributions_dir,
                      test_conf.dz_expenditures_table,
                      test_conf.dz_expenditures_dir)
    ddl.create_tables(test_conf.fz_contributions_table,
                      test_conf.fz_contributions_dir,
                      test_conf.fz_expenditures_table,
                      test_conf.fz_expenditures_dir)

def add_partitions():
    partition = 'batch_id=' + test_conf.batch_id
    ddl.add_partition(test_conf.pz_contributions_table,
                      partition,
                      test_conf.pz_contributions_data_dir + '/' + partition)
    ddl.add_partition(test_conf.pz_expenditures_table,
                      partition,
                      test_conf.pz_expenditures_data_dir + '/' + partition)

if __name__ == '__main__':
    main()
