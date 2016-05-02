#### qa_check.py
Description: Runs the qa_check.hql script and ensure that the result is 0, meaning there are 0 rows in the pz table that aren't in the dz table

Parameters:
* -pz or --pz-table-name - the name of the pz table
* -dz or --dz-table-name - the name of the dz table
* --pz-batch-min - the lower value for the range of partitions in the pz table (inclusive)
* --pz-batch-max - the higher value for the range of partitions in the pz table (inclusive)
