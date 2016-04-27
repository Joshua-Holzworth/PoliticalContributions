#### tests/create_tables_test.py
Tests the creation of LZ tables by running the create_tables.hql script and 
making sure the output has the proper number of "OK" statements. There should be a
 single "OK" for each DDL statement in create_tables.hql

#### tests/add_partition_test.py
Tests the adding of partitions to LZ tables. The first tests in this script
ensure that the DDL statements completed. Then the script runs a select query to 
ensure that the data is actually "in" the external hive table now that a partition
 has been added
