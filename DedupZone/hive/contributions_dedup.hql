INSERT OVERWRITE DIRECTORY '${hiveconf:output_directory}'
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
FROM (
  SELECT * FROM ${hiveconf:pz_table}
  WHERE batch_id >= ${hiveconf:pz_batch_min} AND batch_id <= ${hiveconf:pz_batch_max}
  UNION
  SELECT * FROM ${hiveconf:fz_table}
) as unionResult
GROUP BY report_number, transaction_id
