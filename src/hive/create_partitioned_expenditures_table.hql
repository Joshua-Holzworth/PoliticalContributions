CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

CREATE EXTERNAL TABLE IF NOT EXISTS ${hiveconf:table_name} (
  committee_id string,
  candidate_id string,
  candidate_name string,
  recipient_name string,
  disbursement_amount int,
  disbursement_date string,
  recipient_city string,
  recipient_state string,
  recipient_zip int,
  disbursement_description string,
  memo_code string,
  memo_text string,
  form_type string,
  report_number int,
  transaction_id string,
  election_type string
)
PARTITIONED BY (batch_id string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ","
)
LOCATION '${hiveconf:data_directory}'
