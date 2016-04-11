DROP TABLE ${hiveconf:contributions_table_name};
DROP TABLE ${hiveconf:expenditures_table_name};

CREATE EXTERNAL TABLE ${hiveconf:contributions_table_name} (
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
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ","
)
LOCATION '${hiveconf:contributions_directory}';

CREATE EXTERNAL TABLE ${hiveconf:expenditures_table_name} (
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
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ","
)
LOCATION '${hiveconf:expenditures_directory}';
