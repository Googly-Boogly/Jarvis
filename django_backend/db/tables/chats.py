import os

from global_code.helpful_functions import connect_to_db


class Chat:
    """
    Db class for the chats table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'chats'
        self.db = 'jarvis_db'

        self.chat_id = data.get('chat_id')
        self.title = data.get('title')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')
        self.total_chats_id = data.get('total_chats_id')

    def save(self):
        """saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(title, total_chats_id) ' \
                f'VALUES ("{self.title}", {self.total_chats_id});'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_primary(self, primary_key: int):
        """selects a chat by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE chat_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE chat_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def edit_title(self, new_title: str, primary_key: int):
        """Updates the title field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET title = "{new_title}" ' \
                f'WHERE chat_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement other specific field editing methods as needed
