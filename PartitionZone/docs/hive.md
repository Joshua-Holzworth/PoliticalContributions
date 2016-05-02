#### expenditures_dedup.hql
Description: Unions incoming data (pz) and already stored data (fz), dedups, and stores the result into a new directory

Parameters: see dedup_launch.md

Notes: transaction_id is not a primary key in itself, but report_number and transaction_id are unqiue.
This script groups on the transaction_id and report_number and then selects the first row (if there are duplicates)
with a collect_set(<column>)[0]. Also, hive.support.quoted.identifiers must be set to none so SELECT expressions
can contain regex which is necessary to UNION pz and fz tables because pz has batch_id in its schema and fz
does not so pz must be selected on every column excluding batch_id

#### contributions_dedup.hql
Description: Same as expenditures_dedup.hql except with the proper select statement for contributions
