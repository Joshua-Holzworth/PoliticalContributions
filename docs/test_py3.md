## Test and testing utilities in Python 3
These tests and testing utilities will be mainly for testing hive scripts and 
other processes that require analyzing stdout/stderr for proper completion. A
Test class is also included to help reduce repeated code within tests, and that
can be used for all tests in this project

#### conf.py
Testing configuration variables, such as table names and hdfs paths for LZ, PZ
etc.

#### utils.py
Runs a command and provides methods for checking the count of a specific string
Also provides a method "predicate_on_output" which takes in a predicate function.
That predicate function will receive the output of a command (either stdout or
stderr according to a parameter passed to predicate_on_output) and must return whether
or not the command passed the test

#### tester.py
Includes a python Test class to reduce code common for each test. The Test takes in
a test name and a test function. That test function must return whether or not the
test passed, and then some output to print if the test failed (e.g. stderr)
