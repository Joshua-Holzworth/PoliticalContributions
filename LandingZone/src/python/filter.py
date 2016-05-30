#!/usr/bin/env python2.7
import argparse
import sys
import csv

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SQLContext

import src.python.utils as utils
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

    landing_zone_dir = args.landing_zone + '/batch_id=' + str(args.batch_id)
    filtered_zone_dir = args.filtered_zone + '/batch_id=' + str(args.batch_id)
    filter_cols = [int(x) for x in args.filter_cols.split(',')]

    raw_rdd = get_raw_data(landing_zone_dir)
    split_rdd = raw_rdd.map(lambda x: x.split(','))
    filtered_rdd = raw_rdd.filter(lambda x: filter_nulls(x, filter_cols))
    
    hdfs_utils.rmdir(filtered_zone_dir)
#    hdfs_utils.mkdir(filtered_zone_dir)
    filtered_rdd.saveAsTextFile(filtered_zone_dir + '/')

def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-b', '--batch-id', required=True)
    argparser.add_argument('-l', '--landing-zone', required=True)
    argparser.add_argument('-fz', '--filtered-zone', required=True)
    argparser.add_argument('-fc', '--filter-cols', required=True)
    argparser.add_argument('-pn', '--parent-name', required=True)
    argparser.add_argument('-log', '--log-location', required=True)

    args = argparser.parse_args()

    return args

def get_raw_data(landing_zone):
    if hdfs_utils.files_exist_in_dir(landing_zone):
        return sc.textFile(landing_zone + '/*')
    else:
       utils.log('HDFS dir ' + landing_zone + ' either does not exist or ' +
                 'does not contain any files',
                 LOGGING_NAME, utils.ERROR, LOG_LOCATION)
       sys.exit(1)

def filter_nulls(line, filter_cols):
    cols = csv.reader([line]).next()
    
    for filter_col in filter_cols:
        val = cols[filter_col].strip()

        if not val or val.lower() == 'null':
            return False

    return True

if __name__ == '__main__':
    exit(main())
