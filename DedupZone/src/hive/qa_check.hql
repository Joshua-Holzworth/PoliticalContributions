SELECT COUNT(*) FROM ${hiveconf:pz_table} pz
LEFT JOIN ${hiveconf:dz_table} dz
ON
  pz.report_number = dz.report_number
  AND pz.transaction_id = dz.transaction_id
WHERE 
  pz.batch_id >= '${hiveconf:pz_batch_min}'
  AND pz.batch_id <= '${hiveconf:pz_batch_max}'
  AND dz.report_number IS NULL
  AND dz.transaction_id IS NULL
