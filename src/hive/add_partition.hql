CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

ALTER TABLE ${hiveconf:table_name} ADD IF NOT EXISTS PARTITION (batch_id='${hiveconf:batch_id}')
