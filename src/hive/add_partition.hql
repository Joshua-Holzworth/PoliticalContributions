CREATE DATABASE IF NOT EXISTS contributions;
USE contributions;

ALTER TABLE ${hiveconf:table} ADD IF NOT EXISTS PARTITION (batch_id='${hiveconf:batch_id}')
