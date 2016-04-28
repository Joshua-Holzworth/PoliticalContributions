use ${hiveconf:db_name};

alter table ${hiveconf:table_name} add if not exists partition  (batch_id=${hiveconf:batch_id});
