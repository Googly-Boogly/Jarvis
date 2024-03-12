import os

from global_code.helpful_functions import connect_to_db



class Message:
    """
    Db class for the messages table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'messages'
        self.db = 'jarvis_db'

        self.message_id = data.get('message_id')
        self.model = data.get('model')
        self.agent = data.get('agent')
        self.temp = data.get('temp')
        self.message = data.get('message')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')
        self.chat_id = data.get('chat_id')

    def save(self):
        """saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(model, agent, temp, message, chat_id) ' \
                f'VALUES ("{self.model}", "{self.agent}", {self.temp}, "{self.message}", {self.chat_id});'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_primary(self, primary_key: int):
        """selects a message by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE message_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_where_chat_id(self, primary_key: int):
        """selects a message by its chat key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE chat_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE message_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Example for editing the 'message' field of a record
    def edit_message(self, new_message: str, primary_key: int):
        """Updates the message field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET message = "{new_message}" ' \
                f'WHERE message_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement other specific field editing methods as needed
