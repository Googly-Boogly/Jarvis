import os

from global_code.helpful_functions import connect_to_db


class TotalChats:
    """
    Db class for the total_chats table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'total_chats'
        self.db = 'jarvis_db'

        self.total_chats_id = data.get('total_chats_id')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')

    def save(self) -> int:
        """Saves one instance to the table."""
        query = f'INSERT INTO {self.table_name} ' \
                f'() ' \
                f'VALUES ();'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """Selects all from table."""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_primary(self, primary_key: int):
        """Selects a total_chat by its primary key."""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE total_chats_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """Deletes one instance from the table."""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE total_chats_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # This class might not need an edit_all method as typically only the added and updated timestamps would change,
    # and these can be automatically managed by the database if set up to do so.

    def edit_specific_field(self, field_name: str, field_value: str, primary_key: int):
        """Will edit a specific field of the table given id."""
        query = f'UPDATE {self.table_name} ' \
                f'SET {field_name} = "{field_value}" ' \
                f'WHERE total_chats_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x
