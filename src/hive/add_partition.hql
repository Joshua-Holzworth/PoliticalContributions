ALTER TABLE ${hiveconf:table} ADD IF NOT EXISTS PARTITION (batch_id='${hiveconf:batch_id}')
LOCATION '${hiveconf:partition_path}';
