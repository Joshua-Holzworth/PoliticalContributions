## Test and testing utilities in Python 3

These tests and testing utilities will be mainly for testing hive scripts and other processes that require analyzing stdout/stderr for proper completion

#### test_utils.py
Runs a command and provides methods for checking the count of a specific string
Also provides a method "predicate_on_output" which takes in a predicate function.
That predicate function will receive the output of a command (either stdout or
stderr according to a parameter passed to predicate_on_output) and must return whether
or not the command passed the test

#### create_table_test.py
Runs the create_tables script and ensures the the proper amount of "OK" strings appear
in the output. The idea is that each successfully completed hive DDL statement should
print an "OK" on successful completion
