#!/usr/bin/python3 -B
import src.python.utils as utils
import src.python.ddl as ddl
import test.python.conf as test_conf

def main():
    delete_data()
    drop_tables()

def delete_data():
    command = 'hadoop fs -rm -r ' + test_conf.hdfs_data_root_dir
    utils.run_command(command)

def drop_tables():
    ddl.drop_table(test_conf.pz_contributions_table)
    ddl.drop_table(test_conf.pz_expenditures_table)
    ddl.drop_table(test_conf.dz_contributions_table)
    ddl.drop_table(test_conf.dz_expenditures_table)
    ddl.drop_table(test_conf.fz_contributions_table)
    ddl.drop_table(test_conf.fz_expenditures_table)

if __name__ == '__main__':
    main()
