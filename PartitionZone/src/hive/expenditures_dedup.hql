set hive.support.quoted.identifiers = none;

INSERT OVERWRITE TABLE ${hiveconf:output_table}
SELECT
  collect_set(committee_id)[0],
  collect_set(candidate_id)[0],
  collect_set(candidate_name)[0],
  collect_set(recipient_name)[0],
  collect_set(disbursement_amount)[0],
  collect_set(disbursement_date)[0],
  collect_set(recipient_city)[0],
  collect_set(recipient_state)[0],
  collect_set(recipient_zip)[0],
  collect_set(disbursement_description)[0],
  collect_set(memo_code)[0],
  collect_set(memo_text)[0],
  collect_set(form_type)[0],
  report_number,
  transaction_id,
  collect_set(election_type)[0]
FROM (
  SELECT `(batch_id)?+.+` FROM ${hiveconf:pz_table}
  WHERE batch_id >= '${hiveconf:pz_batch_min}' AND batch_id <= '${hiveconf:pz_batch_max}'
  UNION
  SELECT * FROM ${hiveconf:fz_table}
) as unionResult
GROUP BY report_number, transaction_id
