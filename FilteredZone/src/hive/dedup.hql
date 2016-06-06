CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

INSERT OVERWRITE TABLE ${hiveconf:output_table}
  PARTITION (batch_id=${hiveconf:batch_id})
SELECT 
  fz_committee_id as committee_id,
  fz_candidate_id as candidate_id,
  fz_candidate_name as candidate_name,
  fz_contributor_name as contributor_name,
  fz_contributor_city as contributor_city,
  fz_contributor_state as contributor_state,
  fz_contributor_zip as contributor_zip,
  fz_contributor_employer as contributor_employer,
  fz_contributor_occupation as contributor_occupation,
  fz_contribution_amount as contribution_amount,
  fz_contribution_date as contribution_date,
  fz_receipt_description as receipt_description,
  fz_memo_code as memo_code,
  fz_memo_text as memo_text,
  fz_form_type as form_type,
  rn as report_number,
  tid as transaction_id,
  fz_election_type as election_type
FROM (
  SELECT * FROM (
    SELECT
      collect_set(committee_id)[0] as fz_committee_id,
      collect_set(candidate_id)[0] as fz_candidate_id,
      collect_set(candidate_name)[0] as fz_candidate_name,
      collect_set(contributor_name)[0] as fz_contributor_name,
      collect_set(contributor_city)[0] as fz_contributor_city,
      collect_set(contributor_state)[0] as fz_contributor_state,
      collect_set(contributor_zip)[0] as fz_contributor_zip,
      collect_set(contributor_employer)[0] fz_contributor_employer,
      collect_set(contributor_occupation)[0] fz_contributor_occupation,
      collect_set(contribution_amount)[0] fz_contribution_amount,
      collect_set(contribution_date)[0] fz_contribution_date,
      collect_set(receipt_description)[0] fz_receipt_description,
      collect_set(memo_code)[0] fz_memo_code,
      collect_set(memo_text)[0] fz_memo_text,
      collect_set(form_type)[0] fz_form_type,
      report_number as rn,
      transaction_id as tid,
      collect_set(election_type)[0] as fz_election_type
    FROM ${hiveconf:fz_table}
    WHERE batch_id = ${hiveconf:batch_id}
    GROUP BY report_number, transaction_id
  ) as fz_distinct
  LEFT JOIN ${hiveconf:ez_table} ez
  ON fz_distinct.rn = ez.report_number
    AND fz_distinct.tid = ez.transaction_id
  WHERE ez.report_number IS NULL AND ez.transaction_id IS NULL
) deduped
