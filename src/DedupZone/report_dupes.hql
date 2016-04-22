SELECT report_number, transaction_id, COUNT(*) AS num_contrib FROM ${hiveconf:table}
GROUP BY report_number, transaction_id
HAVING COUNT(*) > 1;
