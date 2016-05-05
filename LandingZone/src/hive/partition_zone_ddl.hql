CREATE DATABASE IF NOT EXISTS partition_zone;

USE partition_zone;


CREATE TABLE IF NOT EXISTS contributions (
  committee_id string,
  candidate_id string,
  candidate_name string,
  contributor_name string,
  contributor_city string,
  contributor_state string,
  contributor_zip int,
  contributor_employer string,
  contributor_occupation string,
  contribution_amount int,
  contribution_date string,
  receipt_description string,
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
LOCATION '${hiveconf:conLoc}';
