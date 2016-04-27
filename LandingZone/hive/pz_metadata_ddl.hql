CREATE DATABASE IF NOT EXISTS partition_zone;

USE partition_zone;

CREATE TABLE IF NOT EXISTS metadata
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