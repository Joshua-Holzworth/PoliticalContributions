from src.python import utils

user = utils.get_user()

batch_id = 'testBatchId'

test_data_root_dir = '/user/' + user + '/test_data'
lz_root_dir = test_data_root_dir + '/LZ'
lz_contributions_data_dir = lz_root_dir + '/contributions'
lz_expenditures_data_dir = lz_root_dir + '/expenditures'
pz_root_dir = test_data_root_dir + '/PZ'
pz_contributions_data_dir = pz_root_dir + '/contributions/data'
pz_contributions_metadata_dir = pz_root_dir + '/contributions/metadata'
pz_expenditures_data_dir = pz_root_dir + '/expenditures/data'
pz_expenditures_metadata_dir = pz_root_dir + '/expenditures/metadata'

lz_contributions_table = 'lz_contributions_test'
lz_expenditures_table = 'lz_expenditures_test'
pz_contributions_table = 'pz_contributions_test'
pz_expenditures_table = 'pz_expenditures_test'
dz_contributions_table = 'dz_contributions_test'
dz_expenditures_table = 'dz_expenditures_test'
fz_contributions_table = 'fz_contributions_test'
fz_expenditures_table = 'fz_expenditures_test'
