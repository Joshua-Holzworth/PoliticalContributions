#!/usr/bin/env python
import sys

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import HiveContext

try:
    input = raw_input
except NameError:
    pass

conf = SparkConf().setAppName('FZ SparkSQL interpreter').setMaster('local')
conf.set('spark.eventLog.enabled', 'true')
sc = SparkContext(conf=conf)
sqlContext = HiveContext(sc)

def main():
    table_name = 'fz_orc'
    sqlContext.sql('USE contributions')
    fz_table = sqlContext.sql('SELECT * FROM ' + table_name)

    while True:
        print('Enter SQL command')
        command = input().rstrip(';')

        try:
            sqlContext.sql(command).show(1000000, truncate=False)
        except Exception:
           e = sys.exc_info()[1]
           print(e)

if __name__ == '__main__':
    main()
