CREATE DATABASE IF NOT EXISTS ${hiveconf:db};
USE ${hiveconf:db};

INSERT OVERWRITE TABLE ${hiveconf:fz_table}
SELECT * FROM ${hiveconf:dz_table};
