from src.python import utils

user = utils.get_user()
project_root_dir = utils.get_project_root_dir()

lz_root_dir = '/user/' + user + '/LZ'
lz_contributions_dir = lz_root_dir + '/contributions'
lz_expenditures_dir = lz_root_dir + '/expenditures'
pz_root_dir = '/user/' + user + '/PZ'
pz_contributions_data_dir = pz_root_dir + '/contributions/data'
pz_contributions_metadata_dir = pz_root_dir + '/contributions/metadata'
pz_expenditures_data_dir = pz_root_dir + '/expenditures/data'
pz_expenditures_metadata_dir = pz_root_dir + '/expenditures/metadata'

lz_contributions_table = 'lz_contributions'
lz_expenditures_table = 'lz_expenditures'
pz_contributions_table = 'pz_contributions'
pz_expenditures_table = 'pz_expenditures'
dz_contributions_table = 'dz_contributions'
dz_expenditures_table = 'dz_expenditures'
fz_contributions_table = 'fz_contributions'
fz_expenditures_table = 'fz_expenditures'

create_tables_script_path = project_root_dir + '/src/hive/create_tables.hql'
create_partitioned_tables_script_path = project_root_dir + '/src/hive/create_partitioned_tables.hql'
drop_table_script_path = project_root_dir + '/src/hive/drop_table.hql'
add_partition_script_path = project_root_dir + '/src/hive/add_partition.hql'
drop_partition_script_path = project_root_dir + '/src/hive/drop_partition.hql'
