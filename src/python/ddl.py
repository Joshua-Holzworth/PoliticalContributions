import src.python.utils as utils
import src.python.conf as conf

def create_contributions_table(table_name, hdfs_data_path):
    command = __get_create_table_command(table_name, hdfs_data_path)
    command += ' -f ' + conf.create_contributions_table_script_path

    utils.log('Creating table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def create_expenditures_table(table_name, hdfs_data_path):
    command = __get_create_table_command(table_name, hdfs_data_path)
    command += ' -f ' + conf.create_expenditures_table_script_path

    utils.log('Creating table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def create_partitioned_contributions_table(table_name, hdfs_data_path):
    command = __get_create_table_command(table_name, hdfs_data_path)
    command += ' -f ' + conf.create_partitioned_contributions_table_script_path

    utils.log('Creating partitioned table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def create_partitioned_expenditures_table(table_name, hdfs_data_path):
    command = __get_create_table_command(table_name, hdfs_data_path)
    command += ' -f ' + conf.create_partitioned_expenditures_table_script_path

    utils.log('Creating partitioned table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def __get_create_table_command(table_name, hdfs_data_path):
    return (
        'hive --hiveconf table_name=' + table_name + 
        ' --hiveconf data_directory=' + hdfs_data_path
        )

def add_partition(table_name, partition):
    command = ('hive --hiveconf table=' + table_name +
               ' --hiveconf batch_id=' + partition +
               ' -f ' + conf.add_partition_script_path)

    utils.log('Adding partition with value ' + partition +
              ' to table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)

def drop_table(table_name):
    command = ('hive --hiveconf table=' + table_name +
               ' -f ' + conf.drop_table_script_path)

    utils.log('Dropping table ' + table_name)
    utils.log(command)
    exit_code, stdout, stderr = utils.capture_command_output(command)
