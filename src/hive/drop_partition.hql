CREATE DATABASE IF NOT EXISTS contributions;
USE contributions;

ALTER TABLE ${hiveconf:table} DROP PARTITION (batch_id=${hiveconf:batch_id});
