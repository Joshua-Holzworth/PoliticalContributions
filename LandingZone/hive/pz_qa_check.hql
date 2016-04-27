USE partition_zone;

SELECT metadata.batch_id, metadata.partition_name, metadata.row_count, data.row_count
FROM
(
 SELECT 
 batch_id, partition_name, row_count
 FROM
 metadata
) metadata
LEFT OUTER JOIN
(
 SELECT 
 batch_id, CONCAT(candidate_id) AS partition_name, COUNT(*) as row_count
 FROM contributions
 GROUP BY 
 batch_id, CONCAT(candidate_id)
 UNION
 SELECT
 batch_id,'TOTAL', COUNT(*)
 FROM ${hiveconf:table_name}
 GROUP BY
 batch_id
) data
ON
metadata.batch_id = data.batch_id and metadata.partition_name = data.partition_name
WHERE metadata.row_count != data.row_count;

