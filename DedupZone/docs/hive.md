#### expenditures_dedup.hql
Description: Unions incoming data (pz) and already stored data (fz), dedups, and stores the result into a new directory

Parameters: see dedup_launch.md

Notes: transaction_id is not a primary key in itself, but report_number and transaction_id are unqiue. This script has been manually test.

#### contributions_dedup.hql
Description: Same as expenditures_dedup.hql except with the proper select statement for contributions
