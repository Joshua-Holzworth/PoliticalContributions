#### expenditures_dedup.hql
Description: Unions incoming data (pz) and already stored data (fz), dedups, and stores the result into a new directory

Parameters: see dedup_launch.md

Notes: transaction_id is not a primary key in itself, but report_number and transaction_id are unqiue.
This script groups on the transaction_id and report_number and then selects the first row (if there are duplicates)
with a collect_set(<column>)[0]

#### contributions_dedup.hql
Description: Same as expenditures_dedup.hql except with the proper select statement for contributions
