#!/usr/local/bin/python3 -B
import src.py3.conf as conf
import src.py3.utils as utils
import test.py3.utils as test_utils
import test.py3.conf as test_conf
from test.py3.tester import Test

NUM_OF_DDL_STATEMENTS = 4

def test_lz_table_creation():
    command = 'hive -hiveconf contributions_directory=' + test_conf.lz_contributions_data_dir
    command += ' --hiveconf expenditures_directory=' + test_conf.lz_expenditures_data_dir
    command += ' --hiveconf contributions_table_name=' + test_conf.lz_contributions_table
    command += ' --hiveconf expenditures_table_name=' + test_conf.lz_expenditures_table
    command += ' -f ' + conf.create_external_tables_script_path
    utils.log('The command being run: \n' + str(command) + '\n')
    
    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)
    output += '\n Contains Count: ' + str(contains_count)

    return test_passed, output

def test_pz_table_creation():
    command = 'hive -hiveconf contributions_directory=' + test_conf.pz_contributions_data_dir
    command += ' --hiveconf expenditures_directory=' + test_conf.pz_expenditures_data_dir
    command += ' --hiveconf contributions_table_name=' + test_conf.pz_contributions_table
    command += ' --hiveconf expenditures_table_name=' + test_conf.pz_expenditures_table
    command += ' -f ' + conf.create_external_tables_script_path
    utils.log('The command being run: \n' + str(command) + '\n')
    
    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)
    output += '\n Contains Count: ' + str(contains_count)

    return test_passed, output

def main():
    lz_table_creation_test = Test('Creation of lz hive tables', test_lz_table_creation)
    pz_table_creation_test = Test('Creation of pz hive tables', test_pz_table_creation)
    lz_table_creation_test.run()
    pz_table_creation_test.run()

if __name__ == '__main__':
    main()
