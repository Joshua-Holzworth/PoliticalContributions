ALTER TABLE ${hiveconf:table} ADD PARTITION (batch_id='${hiveconf:batch_id}')
LOCATION '${hiveconf:partition_path}';
