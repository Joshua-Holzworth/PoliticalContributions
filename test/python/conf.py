import src.python.utils as utils
import src.python.conf as conf

user = utils.get_user()

batch_id = 'testBatchId'

data_path = conf.project_root_dir + '/test/data'
contributions_landing_data_path = data_path + '/original/contributions/data.csv'
expenditures_landing_data_path = data_path + '/original/expenditures/data.csv'
contributions_partitioned_data_path = data_path + '/pz/contributions/data/*'
expenditures_partitioned_data_path = data_path + '/pz/expenditures/data/*'
contributions_partitioned_metadata_path = data_path + '/pz/contributions/metadata/*'
expenditures_partitioned_metadata_path = data_path + '/pz/expenditures/metadata/*'
contributions_result_data_path = data_path + '/original/contributions/sample.csv'
expenditures_result_data_path = data_path + '/original/expenditures/sample.csv'

hdfs_data_root_dir = '/user/' + user + '/test_data'
lz_root_dir = hdfs_data_root_dir + '/LZ'
lz_contributions_data_dir = lz_root_dir + '/contributions'
lz_expenditures_data_dir = lz_root_dir + '/expenditures'
pz_root_dir = hdfs_data_root_dir + '/PZ'
pz_contributions_data_dir = pz_root_dir + '/contributions/data'
pz_contributions_metadata_dir = pz_root_dir + '/contributions/metadata'
pz_expenditures_data_dir = pz_root_dir + '/expenditures/data'
pz_expenditures_metadata_dir = pz_root_dir + '/expenditures/metadata'
dz_root_dir = hdfs_data_root_dir + '/DZ'
dz_contributions_dir = dz_root_dir + '/contributions'
dz_expenditures_dir = dz_root_dir + '/expenditures'
fz_root_dir = hdfs_data_root_dir + '/FZ'
fz_contributions_dir = fz_root_dir + '/contributions'
fz_expenditures_dir = fz_root_dir + '/expenditures'

pz_contributions_table = 'pz_contributions_test'
pz_expenditures_table = 'pz_expenditures_test'
dz_contributions_table = 'dz_contributions_test'
dz_expenditures_table = 'dz_expenditures_test'
fz_contributions_table = 'fz_contributions_test'
fz_expenditures_table = 'fz_expenditures_test'
