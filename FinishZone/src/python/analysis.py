#!/usr/bin/env python
from pyspark import SparkContext
from pyspark.sql import HiveContext

sc = SparkContext('local', 'Simple app')
sqlContext = HiveContext(sc)

def main():
    sqlContext.sql('USE contributions')
    fz_table = sqlContext.sql('SELECT * FROM fz')

    # count_contributors(fz_table)
    contribution_stats()

def count_contributors(contributions):
    print('Candidates and number of contributions')
    (contributions.groupBy('candidate_id', 'candidate_name')
        .count()
        .orderBy('count', ascending=False)
        .show(100, False))

def contribution_stats():
    print('Candidates and amount of contributions')

    select_expression = ('SELECT candidate_id, candidate_name, ' +
                         'CONCAT("$", CAST(ROUND(SUM(CAST(contribution_amount AS DECIMAL)), 2) AS DECIMAL)) as amount, ' +
                         'COUNT(*) as num_of_contributions, ' + 
                         'CONCAT("$", MAX(CAST(contribution_amount AS DECIMAL))) as max_contribution, ' + 
                         'CONCAT("$", ROUND(AVG(CAST(contribution_amount AS DECIMAL)), 2)) as avg_contribution ' + 
                         'FROM fz GROUP BY candidate_id, candidate_name ' +
                         'ORDER BY CAST(SUBSTRING(amount, 2) AS DECIMAL) DESC')

    print('Command: ' + str(select_expression))

    sqlContext.sql(select_expression).show(100, False)

if __name__ == '__main__':
    exit(main())
