#### connector.py
A context manager for connecting to hbase. The \_\_enter\_\_ and \_\_exit\_\_ allow objects of this class to 
be used with python "with" statements

#### data\_access\_layer.py
Description: a DAL for hbase. Has an outward facing api (get\_step\_batch, set\_step\_to\_stopped, etc)
and is implemented with a functional style of programming. 

Design: Each operation that is performed on the hbase table is done through the internal method 
\_\_operate\_on\_table. This method takes in a function, opens up a connection to hbase, grabs 
the table that the DAL was contructed with, and then calls that function with the table as an argument.
This reduces duplicate code as each function in the API can focus solely on the logic it performs on the
table (as opposed to each function having to include the code for opening the connection) and it allows
multiple operations to be performed on the connection without having to close and reopen the connection.
As an example, look at \_\_set\_step\_to\_stopped. This method consists of getting the row key for the
latest step and then updating some data in that row. If each method individually opened up a connection
to hbase, this would result in \_\_get\_latest\_step\_row\_key opening a connection, grabbing the table, 
getting the step's latest row key, and closing the connection before returning the row key, then 
\_\_set\_step\_to\_stopped would have to open a connection, grab the table, grab the row, update the data,
then close the connection. With this design, \_\_operate\_on\_table opens a connection, grabs the table,
and then passes the table to \_\_set\_step\_to\_stopped (the func argument to \_\_operate\_on\_table in this
case). \_\_set\_step\_to\_stopped can then use that table to get the row key, get the row, then update the
data. \_\_operate\_on\_table would then close the connection. All of this requires one open connection
operation, and a single get of the table.

Because each callback function passed into \_\_operate\_on\_table might take in more arguments than
just the table, functools.partial is imported as bind. It is aliased as bind because it behaves the same
way bind does in javascript, and it seemed more expressive that way. functools.partial will "bind"
arguments to a function and return a new function that has a new method signature without all of the
parameters that have just been bound. For example, if you have a function f(a, b) and you call 
functools.partial(f, 2), that call to functools.partial will return a new function (let's call it g)
with the signature g(b). If you make a call to g, it will essentially be a call to f with the value
"2" bound to parameter "a", and whatever is passed in to g for the paremeter b will be what's passed
into parameter b for function f 

Constructor Params:
* connector - Connector instance that DAL will use to connect to hbase
* table_name - name of table this DAL will use
