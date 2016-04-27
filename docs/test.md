## Tests and testing information
Individual tests can be found in PROJECT_ROOT/test/tests.
The tests require some data to test on, so a setup and teardown script is included

#### data_setup.py
Description: Prepares testing data by creating folders in hdfs and putting test data into them

Parameters:
* -c or --contributions-path - the local path to the contributions data 
* -e or --expenditures-path - the local path to the expenditures data 

#### data_teardown.py
Removes the testing folders and data from hdfs
