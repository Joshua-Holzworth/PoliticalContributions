CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

CREATE TABLE ${hiveconf:output_table}
STORED AS ORC
AS
SELECT
  committee_id,
  candidate_id,
  candidate_name,
  contributor_name,
  contributor_city,
  contributor_state,
  CAST(contributor_zip AS DECIMAL) AS contributor_zip,
  contributor_employer,
  contributor_occupation,
  CAST(ROUND(CAST(contribution_amount AS DECIMAL), 2) AS DECIMAL) AS contribution_amount,
  CAST(to_date(from_unixtime(UNIX_TIMESTAMP(contribution_date, 'dd-MMM-yy'))) AS date) AS contribution_date,
  receipt_description,
  memo_code,
  memo_text,
  form_type,
  report_number,
  transaction_id,
  election_type
FROM ${hiveconf:fz_table};
