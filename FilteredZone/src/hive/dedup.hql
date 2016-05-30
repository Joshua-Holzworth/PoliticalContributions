CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

set hive.support.quoted.identifiers = none;

INSERT OVERWRITE TABLE ${hiveconf:output_table}
  PARTITION (batch_id=${hiveconf:batch_id})
SELECT * FROM (
  SELECT
    collect_set(committee_id)[0],
    collect_set(candidate_id)[0],
    collect_set(candidate_name)[0],
    collect_set(contributor_name)[0],
    collect_set(contributor_city)[0],
    collect_set(contributor_state)[0],
    collect_set(contributor_zip)[0],
    collect_set(contributor_employer)[0],
    collect_set(contributor_occupation)[0],
    collect_set(contribution_amount)[0],
    collect_set(contribution_date)[0],
    collect_set(receipt_description)[0],
    collect_set(memo_code)[0],
    collect_set(memo_text)[0],
    collect_set(form_type)[0],
    report_number,
    transaction_id,
    collect_set(election_type)[0]
  FROM ${hiveconf:fz_table}
  WHERE batch_id = ${hiveconf:batch_id}
  GROUP BY report_number, transaction_id
) as fz_distinct
LEFT JOIN ${hiveconf:ez_table} ez
ON fz_distinct.report_number = ez.report_number
  AND fz_distinct.transaction_id = ez.transaction_id
WHERE ez.report_number IS NULL AND ez.transaction_id IS NULL
