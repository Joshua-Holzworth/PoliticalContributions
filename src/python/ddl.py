import src.python.utils as utils
import src.python.conf as conf

def create_tables(contributions_table_name, contributions_hdfs_data_path,
                  expenditures_table_name, expenditures_hdfs_data_path):

    command = __get_create_tables_command(contributions_table_name,
                                       contributions_hdfs_data_path,
                                       expenditures_table_name,
                                       expenditures_hdfs_data_path)
    command += ' -f ' + conf.create_tables_script_path

    utils.log('Creating tables ' + contributions_table_name +
              ' and ' + expenditures_table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def create_partitioned_tables(contributions_table_name,
                              contributions_hdfs_data_path,
                              expenditures_table_name,
                              expenditures_hdfs_data_path):

    command = __get_create_tables_command(contributions_table_name,
                                       contributions_hdfs_data_path,
                                       expenditures_table_name,
                                       expenditures_hdfs_data_path)
    command += ' -f ' + conf.create_partitioned_tables_script_path

    utils.log('Creating tables ' + contributions_table_name +
              ' and ' + expenditures_table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def __get_create_tables_command(contributions_table_name,
                                contributions_hdfs_data_path,
                                expenditures_table_name,
                                expenditures_hdfs_data_path):
    return (
        'hive --hiveconf contributions_table_name=' + 
	contributions_table_name + 
        ' --hiveconf expenditures_table_name=' + 
        expenditures_table_name +
        ' --hiveconf expenditures_directory=' + 
        expenditures_hdfs_data_path +
        ' --hiveconf contributions_directory=' + 
        contributions_hdfs_data_path
        )

def add_partition(table_name, partition, partition_path):
    command = ('hive --hiveconf table=' + table_name +
               ' --hiveconf batch_id=' + partition +
               ' --hiveconf partition_path=' + partition_path +
               ' -f ' + conf.add_partition_script_path)

    utils.log('Adding partition with value ' + partition +
              ' to table ' + table_name + ' located at path ' + partition_path)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def drop_table(table_name):
    command = ('hive --hiveconf table=' + table_name +
               ' -f ' + conf.drop_table_script_path)

    utils.log('Dropping table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)
