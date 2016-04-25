#### expenditures_dedup.hql
Description: Unions incoming data (pz) and already stored data (fz), dedups, and stores the result into a new directory

Parameters:
* output_directory - the directory where the deduped data will go (e.g. '/user/root/DZ/tfz')
* pz_table - name of pz table
* fz_table - name of fz table
* pz_batch_min - lowest batch partition to query on (inclusive)
* pz_batch_max - highest batch partition to query on (inclusive)


Notes: transaction_id is not a primary key in itself, but report_number and transaction_id are unqiue. This script has been manually test.

#### contributions_dedup.hql
Description: Same as expenditures_dedup.hql except with the proper select statement for contributions
