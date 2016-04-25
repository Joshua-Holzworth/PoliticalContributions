"""
Tests create_tables.hql. Each DDL statement in that script should print out an "OK"
to stderr if it is completed correctly. To test this script, we check that the
number of "OK"s in the output is equal to the number of DDL statements in the script

Author: Garrett Holbrook
"""

import subprocess
import shlex
import test_utils

NUM_OF_DDL_STATEMENTS = 4
TEST_ACTION_DESCRIPTION = 'Creation of hive tables' # TEST_ACTION_DESCRIPTION means a description of what exactly we are testing

batchId = '_createTableTestBatch' # arbitrary batch id
contributions_table_name = 'contributions' + str(batchId)
contributions_directory = '/user/root/LZ/contibutions'
expenditures_table_name = 'expenditures' + str(batchId)
expenditures_directory = '/user/root/LZ/expenditures'
table_creation_script_path = '../../src/HiveDDL/create_tables.hql'

command = 'hive -hiveconf contributions_directory=' + contributions_directory
command += ' --hiveconf expenditures_directory=' + expenditures_directory
command += ' --hiveconf contributions_table_name=' + contributions_table_name
command += ' --hiveconf expenditures_table_name=' + expenditures_table_name
command += ' -f ' + table_creation_script_path
print('The command being run: \n' + str(command) + '\n')

test_passed, output, contains_count = test_utils.output_contains_exactly(command, 'OK', NUM_OF_DDL_STATEMENTS, check_stderr=True)

if test_passed:
    print('Test \"' + TEST_ACTION_DESCRIPTION + '\" passed')
else:
    print('Test \"' + TEST_ACTION_DESCRIPTION + '\" failed!')
    print('Output from command:')
    print(output)
