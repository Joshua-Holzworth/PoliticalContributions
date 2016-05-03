INSERT OVERWRITE TABLE ${hiveconf:fz_table}
SELECT * FROM ${hiveconf:dz_table};
