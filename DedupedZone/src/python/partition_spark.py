#!/usr/bin/env python2.7
import argparse
import sys
import csv

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SQLContext

import src.python.hdfs_utils as hdfs_utils

LOGGING_NAME = 'filter.py'
LOG_LOCATION = None

conf = SparkConf().setAppName('LZ Filtering').setMaster('local')
conf.set('spark.eventLog.enabled', 'true')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def main():
    args = parse_args()

    global LOGGING_NAME, LOG_LOCATION
    LOGGING_NAME = args.parent_name + ' ' + LOGGING_NAME
    LOG_LOCATION = args.log_location

    landing_zone_dir = args.landing_zone + '/' + 'batch_id=' + str(args.batch_id)
    filter_cols = [int(x) for x in args.filter_cols.split(',')]

    raw_rdd = get_raw_data(landing_zone_dir)
    split_rdd = raw_rdd.map(lambda x: x.split(','))
    filtered_rdd = raw_rdd.filter(lambda x: filter_nulls(x, filter_cols))

#    split_df = sqlContext.createDataFrame(split_rdd)
#    new_df = split_df.where('_20 = ""')
#    print(split_df.count())
#    print(new_df.count())
#    split_df.write.save(path=landing_zone_dir, format='text', filterBy=('_' + args.filter_col))

    # write_metadata(args.transition_zone, args.batch_id)

#    push_to_pz(args.transition_zone, args.filter_zone)
#    cleanup(local_landing_zone)
#    cleanup(args.transition_zone)

if __name__ == '__main__':
    exit(main())
