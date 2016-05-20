#!/usr/bin/env python
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import HiveContext

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
        command = raw_input().rstrip(';')
        sqlContext.sql(command).show(1000000, truncate=False)

if __name__ == '__main__':
    main()
