CREATE DATABASE IF NOT EXISTS ${hiveconf:db};

USE ${hiveconf:db};

CREATE EXTERNAL TABLE IF NOT EXISTS metadata
(
partition_name string,
row_count int
)
PARTITIONED BY (batch_id string)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '${hiveconf:metadataLoc}';
