CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

CREATE EXTERNAL TABLE IF NOT EXISTS ${hiveconf:table_name} (
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
STORED AS ORC
LOCATION '${hiveconf:data_directory}';
