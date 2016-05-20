#!/usr/bin/env python
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import HiveContext

conf = SparkConf().setAppName('FZ Analysis').setMaster('local')
conf.set('spark.eventLog.enabled', 'true')
sc = SparkContext(conf=conf)
sqlContext = HiveContext(sc)

def main():
    table_name = 'fz_orc'
    sqlContext.sql('USE contributions')
    fz_table = sqlContext.sql('SELECT * FROM ' + table_name)

    contribution_stats_command = contribution_stats(table_name)
    top_occupations_command = top_occupations(table_name)
    top_date_command = top_date(table_name)
    top_states_command = top_states(table_name)
    top_employers_command = top_employers(table_name)

    print('Contributions Stats')
    sqlContext.sql(contribution_stats_command).show(1000000, truncate=False)
    print('Top 5 occupations per candidate')
    sqlContext.sql(top_occupations_command).show(1000000, truncate=False)
    print('Top 2 dates per candidate')
    sqlContext.sql(top_date_command).show(1000000, truncate=False)
    print('Top 5 states per candidate')
    sqlContext.sql(top_states_command).show(1000000, truncate=False)
    print('Top 10 employers per candidate')
    sqlContext.sql(top_employers_command).show(1000000, truncate=False)

def count_contributors(contributions):
    print('Candidates and number of contributions')
    (contributions.groupBy('candidate_id', 'candidate_name')
        .count()
        .orderBy('count', ascending=False)
        .show(100, False))

def contribution_stats(table_name):
    return '''
           SELECT candidate_name, 
             CONCAT("$", SUM(total_amount)) as amount, 
             COUNT(*) as num_of_contributions, 
             CONCAT("$", MAX(max_contribution)) as max_contribution,   
             CONCAT("$", ROUND(AVG(total_amount), 2)) as avg_contribution 
           FROM ( 
             SELECT candidate_name, 
               COUNT(*) as num_of_contributions,
               SUM(contribution_amount) as total_amount,
               MAX(contribution_amount) as max_contribution
             FROM ''' + table_name + '''
             GROUP BY candidate_name, contributor_name, contributor_zip,
             contributor_employer, contributor_occupation
           ) tmp
           GROUP BY candidate_name
           ORDER BY CAST(SUBSTRING(amount, 2) AS DECIMAL) DESC'''

def top_occupations(table_name):
    return '''
           SELECT
             candidate_name,
             contributor_occupation,
             CONCAT("$", total_amount) as total_amount,
             rnk
           FROM (
             SELECT
               candidate_name,
               contributor_occupation,
               total_amount,
               dense_rank() over (PARTITION BY candidate_name ORDER BY total_amount DESC) as rnk  
             FROM (
               SELECT 
                 candidate_name,
                 contributor_occupation, 
                 SUM(contribution_amount) as total_amount
               FROM ''' + table_name + '''
               WHERE contributor_occupation != ""  
               GROUP BY candidate_name, contributor_occupation
               ) a  
             ) b  
           WHERE rnk <= 5'''

def top_states(table_name):
    return '''
           SELECT
             candidate_name,
             contributor_state,
             CONCAT("$", total_amount) as total_amount,
             rnk
           FROM (
             SELECT
               candidate_name,
               contributor_state,
               total_amount,
               dense_rank() over (PARTITION BY candidate_name ORDER BY total_amount DESC) as rnk  
             FROM (
               SELECT 
                 candidate_name,
                 contributor_state, 
                 SUM(contribution_amount) as total_amount
               FROM ''' + table_name + '''
               WHERE contributor_state != ""  
               GROUP BY candidate_name, contributor_state
               ) a  
             ) b  
           WHERE rnk <= 5'''

def top_date(table_name):
    return '''
           SELECT
             candidate_name,
             contribution_date,
             CONCAT("$", total_amount) as total_amount,
             rnk
           FROM (
             SELECT
               candidate_name,
               contribution_date,
               total_amount,
               dense_rank() over (PARTITION BY candidate_name ORDER BY total_amount DESC) as rnk  
             FROM (
               SELECT 
                 candidate_name,
                 contribution_date, 
                 SUM(contribution_amount) as total_amount
               FROM ''' + table_name + '''
               WHERE contribution_date != ""  
               GROUP BY candidate_name, contribution_date
               ) a  
             ) b  
           WHERE rnk <= 2'''

def top_employers(table_name):
    return '''
           SELECT
             candidate_name,
             contributor_employer,
             CONCAT("$", total_amount) as total_amount,
             rnk
           FROM (
             SELECT
               candidate_name,
               contributor_employer,
               total_amount,
               dense_rank() over (PARTITION BY candidate_name ORDER BY total_amount DESC) as rnk  
             FROM (
               SELECT 
                 candidate_name,
                 contributor_employer, 
                 SUM(contribution_amount) as total_amount
               FROM ''' + table_name + '''
               WHERE contributor_employer != ""  
               GROUP BY candidate_name, contributor_employer
               ) a  
               WHERE total_amount > 10800
               AND contributor_employer NOT LIKE '%REQUESTED%'
             ) b  
           WHERE rnk <= 10
           '''

if __name__ == '__main__':
    main()
