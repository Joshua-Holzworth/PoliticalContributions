CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

SELECT COUNT(*) FROM ${hiveconf:fz_table} fz
LEFT JOIN ${hiveconf:dz_table} dz
ON
  fz.report_number = dz.report_number
  AND fz.transaction_id = dz.transaction_id
WHERE 
  fz.batch_id == '${hiveconf:batch_id}'
  AND dz.report_number IS NULL
  AND dz.transaction_id IS NULL
  AND fz.report_number IS NOT NULL
  AND fz.transaction_id IS NOT NULL
