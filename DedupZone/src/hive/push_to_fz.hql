CREATE DATABASE IF NOT EXISTS contributions;
USE contributions;

INSERT OVERWRITE TABLE ${hiveconf:fz_table}
SELECT * FROM ${hiveconf:dz_table};
