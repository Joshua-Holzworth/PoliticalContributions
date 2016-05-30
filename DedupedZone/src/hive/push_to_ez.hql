CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

INSERT INTO TABLE ${hiveconf:ez_table}
SELECT * FROM ${hiveconf:dz_table} dz
WHERE dz.batch_id = '${hiveconf:batch_id}'
