


Parsing:

Consume a directory. Read in base level files (So no multiple depth directory traversal).

Loop over each file in the root directory given and read in each one. 
Depending on specified partition columns parse the row and write into another file (and output directory).

While looping over each file and re structuring the data, keeps track of row counts and total row counts.

Once all files are finished processing writes out a metadata file with TOTAL and all other partition values and their respective counts.


Output directories follow the following structure.

{ROOT} / {DATA or METADATA} / {BATCHID} / {PARTITION} / {FILENAME}

An example of a few data files and their complete directories is listed below.

/rootDir/data/bid1234/clinton/bid1234.csv
/rootDir/data/bid1234/obama/bid1234.csv

An example of respective metadata for all files listed above.

/rootDir/metadata/bid1234/metadata.csv