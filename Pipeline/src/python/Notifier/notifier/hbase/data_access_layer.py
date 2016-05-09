from functools import partial as bind

class DataAccessLayer():
    def __init__(self, connector, table_name):
        self.connector = connector
        self.table_name = table_name

    def get_step_batch(self, step_name, batch_id):
        row_key = self.__build_row_key(step_name, batch_id)

        func = bind(self.__get_step_batch, row_key)
        return self.__operate_on_table(func)

    def get_latest_step_batch(self, step_name):
        func = bind(self.__get_latest_step_batch, step_name)
        return self.__operate_on_table(func)

    def get_latest_batch_id(self, step_name):
        row_key = self.get_latest_step_batch(step_name)[0]
        batch_id = self.__decode_row_key(row_key)[1]

        return batch_id
    
    def set_step_to_running(self, step_name, start_message):
        func = bind(self.__set_step_to_running, step_name, start_message)
        self.__operate_on_table(func)

    def set_step_to_stopped(self, step_name, end_message):
        func = bind(self.__set_step_to_stopped, step_name, end_message)
        self.__operate_on_table(func)

    def increment_step(self, step_name):
        func = bind(self.__increment_step, step_name)
        self.__operate_on_table(func)

    def __operate_on_table(self, func):
        with self.connector as connection:
            table = connection.table(self.table_name)
            return func(table)

    def __get_step_batch(self, row_key, table):
        return table.row(row_key)

    def __get_latest_step_batch(self, step_name, table):
        return table.scan(row_prefix=step_name).next()

    def __get_latest_step_row_key(self, step_name, table):
        return self.__get_latest_step_batch(step_name, table)[0]

    def __get_latest_step_batch_id(self, step_name, table):
        row_key = self.__get_latest_step_row_key(step_name, table)
        return self.__decode_row_key(row_key)[1]

    def __set_step_to_stopped(self, step_name, end_message, table):
        row_key = self.__get_latest_step_row_key(step_name, table)

        row = table.row(row_key)
        status = row.get('current:status')

        if status == 'Running' or status == 'Stopped':
            current_attempt_num = int(row.get('current:attemptNum'))
            update_data = {
                'attemptEnd:' + str(current_attempt_num) : str(end_message),
                'current:status' : 'Stopped'
            }
            table.put(row_key, update_data)

    def __set_step_to_running(self, step_name, start_message, table):
        row_key = self.__get_latest_step_row_key(step_name, table)

        row = table.row(row_key)
        status = row.get('current:status')

        if status != 'Running' and status != 'Started':
            new_attempt_num = int(row.get('current:attemptNum') or 0) + 1
            update_data = {
                'attemptStart:' + str(new_attempt_num) : str(start_message),
                'current:status' : 'Running',
                'current:attemptNum': str(new_attempt_num)
            }
            table.put(row_key, update_data)

    def __increment_step(self, step_name, table):
        current_row_key = self.__get_latest_step_row_key(step_name, table)
        current_step_batch_id = self.__decode_row_key(current_row_key)[1]
        next_batch_id = self.__get_next_batch_id(current_step_batch_id)
        next_row_key = self.__build_row_key(step_name, next_batch_id)

        table.put(next_row_key, {
            'current:status': 'Stopped',
            'current:attemptNum': '0'
        })

    def __build_row_key(self, step_name, batch_id):
        return str(step_name) + '.' + str(batch_id)

    def __decode_row_key(self, row_key):
        return tuple(row_key.split('.'))

    def __get_next_batch_id(self, batch_id):
        return batch_id - 1
