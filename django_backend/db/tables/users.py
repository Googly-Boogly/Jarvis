import os

from global_code.helpful_functions import connect_to_db, create_logger_error, log_it

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='users',
                             log_to_console=True, log_to_file=False)

class User:
    """
    Db class for the users table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'users'
        self.db = 'jarvis_db'

        self.user_id = data.get('user_id')
        self.password = data.get('password')
        self.name = data.get('name')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')
        self.total_chats_id = data.get('total_chats_id')

    def save(self):
        """saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(password, name, total_chats_id) ' \
                f'VALUES ("{self.password}", "{self.name}", {self.total_chats_id});'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        log_it(logger=logger, error=None, custom_message=f"USER SELECT: {x}", log_level="info")
        return x

    def select_one_for_primary(self, primary_key: int):
        """selects a user by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE user_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE user_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Example for updating the 'name' field of a user
    def edit_name(self, new_name: str, primary_key: int):
        """Updates the name field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET name = "{new_name}" ' \
                f'WHERE user_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement other specific field editing methods as needed
