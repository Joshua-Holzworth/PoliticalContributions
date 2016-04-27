## Tests and testing information
Individual tests can be found in PROJECT_ROOT/test/tests.
The tests require some data to test on, so a setup and teardown script is included

#### data_setup.py
Description: Prepares testing data by creating folders in hdfs and putting test data into them

Parameters:
* -c or --contributions-path - the local path to the contributions data 
* -e or --expenditures-path - the local path to the expenditures data 

#### data_teardown.py
Removes the testing folders and data from hdfs

#### tests/create_tables_test.py
Tests the creation of LZ and PZ tables by running the create_tables.hql script and 
making sure the output has the proper number of "OK" statements. There should be a
 single "OK" for each DDL statement in create_tables.hql

#### tests/add_partition_test.py
Tests the adding of partitions to LZ and PZ tables. The first tests in this script
ensure that the DDL statements completed. Then the script runs a select query to 
ensure that the data is actually "in" the external hive table now that a partition
 has been added
