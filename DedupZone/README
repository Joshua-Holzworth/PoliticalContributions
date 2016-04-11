#### dedup.hql
Description: Stores all non-duplicate rows into a new directory
Parameters:
* output_directory - the directory where the deduped data will go (e.g. '/user/root/DZ/expenditures/batch9229')
* table - the table to dedup (e.g. pz_expenditures_batch9229)
Notes: transaction_id is not a primary key in itself, but report_number and transaction_id are unqiue. This script has been manually test.

#### report_dupes.hql
Description: Report all duplicates in a table
Parameters:
* table - the table to dedup
Notes: Not general purpose, works for contributions and expenditures tables
