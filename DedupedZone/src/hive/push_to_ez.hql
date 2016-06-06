CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

set hive.support.quoted.identifiers = none;

INSERT INTO TABLE ${hiveconf:ez_table}
SELECT `(batch_id)?+.+` FROM ${hiveconf:dz_table} dz
WHERE dz.batch_id = '${hiveconf:batch_id}'
