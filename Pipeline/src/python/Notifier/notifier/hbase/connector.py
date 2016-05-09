import happybase

class Connector():
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def __enter__(self):
        self.connection = happybase.Connection(self.connection_string)
        self.connection.open()
        return self.connection

    def __exit__(self, *exception_args):
        self.connection.close()
