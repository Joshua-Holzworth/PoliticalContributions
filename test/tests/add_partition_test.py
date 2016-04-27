#!/usr/local/bin/python3 -B
import src.py3.utils as utils
import src.py3.conf as conf
import test.py3.utils as test_utils
import test.py3.conf as test_conf
from test.py3.tester import Test

NUM_OF_DDL_STATEMENTS = 1
NUM_OF_FETCHED_OCCURRENCES = 1 # Number of times the string "Fetched" should occur in output

def test_pz_contributions_partition_add():
    command = 'hive --hiveconf table=' + test_conf.pz_contributions_table 
    command += ' --hiveconf batch_id=' + test_conf.batch_id
    command += ' --hiveconf partition_path=' + test_conf.pz_contributions_data_dir + '/' + test_conf.batch_id
    command += ' -f ' + conf.add_partition_script_path
    
    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)

    return test_passed, output
    

def test_pz_expenditures_partition_add():
    command = 'hive --hiveconf table=' + test_conf.pz_expenditures_table
    command += ' --hiveconf batch_id=' + test_conf.batch_id
    command += ' --hiveconf partition_path=' + test_conf.pz_expenditures_data_dir + '/' + test_conf.batch_id
    command += ' -f ' + conf.add_partition_script_path
    
    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)

    return test_passed, output

def test_lz_contributions_partition_add():
    command = 'hive --hiveconf table=' + test_conf.lz_contributions_table 
    command += ' --hiveconf batch_id=' + test_conf.batch_id
    command += ' --hiveconf partition_path=' + test_conf.lz_contributions_data_dir + '/' + test_conf.batch_id
    command += ' -f ' + conf.add_partition_script_path
    
    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)

    return test_passed, output
    

def test_lz_expenditures_partition_add():
    command = 'hive --hiveconf table=' + test_conf.lz_expenditures_table
    command += ' --hiveconf batch_id=' + test_conf.batch_id
    command += ' --hiveconf partition_path=' + test_conf.lz_expenditures_data_dir + '/' + test_conf.batch_id
    command += ' -f ' + conf.add_partition_script_path
    
    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)

    return test_passed, output

def test_data_in_lz_contributions_table():
    command = "hive -e 'SELECT * FROM " + test_conf.lz_contributions_table + " LIMIT 1'"

    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'Fetched', NUM_OF_FETCHED_OCCURRENCES, check_stderr=True)
    return test_passed, output

def test_data_in_lz_expenditures_table():
    command = "hive -e 'SELECT * FROM " + test_conf.lz_expenditures_table + " LIMIT 1'"

    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'Fetched', NUM_OF_FETCHED_OCCURRENCES, check_stderr=True)
    return test_passed, output

def test_data_in_pz_contributions_table():
    command = "hive -e 'SELECT * FROM " + test_conf.pz_contributions_table + " LIMIT 1'"

    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'Fetched', NUM_OF_FETCHED_OCCURRENCES, check_stderr=True)
    return test_passed, output

def test_data_in_pz_expenditures_table():
    command = "hive -e 'SELECT * FROM " + test_conf.pz_expenditures_table + " LIMIT 1'"

    utils.log('The command being run: \n' + str(command) + '\n')

    test_passed, exit_code, output, contains_count = test_utils.output_contains_exactly(command, 'Fetched', NUM_OF_FETCHED_OCCURRENCES, check_stderr=True)
    return test_passed, output


def main():
    lz_contributions_partition_add_test = Test('Adding partition to LZ contributions table', test_lz_contributions_partition_add)
    lz_expenditures_partition_add_test = Test('Adding partition to LZ expenditures table', test_lz_expenditures_partition_add)
    pz_contributions_partition_add_test = Test('Adding partition to PZ contributions table', test_pz_contributions_partition_add)
    pz_expenditures_partition_add_test = Test('Adding partition to PZ expenditures table', test_pz_expenditures_partition_add)

    lz_contributions_data_in_table_test = Test('Ensuring data exists in LZ contributions table now that partition has been added', test_data_in_lz_contributions_table)
    lz_expenditures_data_in_table_test = Test('Ensuring data exists in LZ expenditures table now that partition has been added', test_data_in_lz_expenditures_table)
    pz_contributions_data_in_table_test = Test('Ensuring data exists in PZ contributions table now that partition has been added', test_data_in_pz_contributions_table)
    pz_expenditures_data_in_table_test = Test('Ensuring data exists in PZ expenditures table now that partition has been added', test_data_in_pz_expenditures_table)

    lz_contributions_partition_add_test.run()
    lz_expenditures_partition_add_test.run()
    pz_contributions_partition_add_test.run()
    pz_expenditures_partition_add_test.run()
    lz_contributions_data_in_table_test.run()
    lz_expenditures_data_in_table_test.run()
    pz_contributions_data_in_table_test.run()
    pz_expenditures_data_in_table_test.run()

if __name__ == '__main__':
    main()
