## Hive DDL scripts
Scripts for hive DDL. Can be found in PROJECT_ROOT/hive

#### create_tables.hql
Description: Creates two external hive tables, one for contributions and one for expenditures based

Parameters:
* contributions_table_name - how this contributions table will be named in the hive metastore. (e.g. lz_contributions_batch2343)
* expenditures_table_name - same as above but for expenditures
* expenditures_table_name - same as above but for expenditures
* expenditures_directory - same as above but for expenditures

Notes: Because the data has commas enclosed in quotation marks at the same time that commas are used for delimiting the data (e.g. "Rubio, Marco", "SA1843")
a SerDe is required. The one used is the built in (hive 0.14+) OpenCSVSerde. Even though the table definitions contain ints, this SerDe casts all values
to strings in an outstanding act of poor code design. If you run DESCRIBE <table_name> it will list every column as being of type string. If data types
end up being important, a hive view that casts every field into its proper data type should be considered.

#### create_external_tables.hql
Description: Same as create_tables, but the tables are partitioned

#### add_partition.hql
Parameters:
* table - table name
* batch_id - the batch id of the partition to be added 
* partition_path - location of partition being added

#### drop_partition.hql
Parameters:
* table - table name
* batch_id - the batch id of the partition to be removed

#### drop_table.hql
Parameters:
* table - table name to drop
