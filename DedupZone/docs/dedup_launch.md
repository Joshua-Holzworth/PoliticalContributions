#### dedup_launch.py
Description: Launches the dedup scripts using python 3

Parameters:
* --output_table - the table where the deduped data will go
* --pz_table - name of pz table
* --fz_table - name of fz table
* --pz_batch_min - lowest batch partition to query on (inclusive)
* --pz_batch_max - highest batch partition to query on (inclusive)

Notes:
Each argument is required. Run dedup_launch.py -h for help
