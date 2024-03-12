import os

from global_code.helpful_functions import connect_to_db, create_logger_error, log_it

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='functions',
                             log_to_console=True, log_to_file=False)

class Function:
    """
    Db class for the functions table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'functions'
        self.db = 'jarvis_db'

        self.function_id = data.get('function_id')  # Auto-increment field
        self.function_name = data.get('function_name')
        self.function_description = data.get('function_description')
        self.function_inputs = data.get('function_inputs')
        self.function_output = data.get('function_output')
        self.function_json = data.get('function_json')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')

    def save(self):
        """Saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(function_name, function_description, function_inputs, function_output, function_json) ' \
                f'VALUES ("{self.function_name}", "{self.function_description}", "{self.function_inputs}", ' \
                f'"{self.function_output}", "{self.function_json}");'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """Selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        log_it(logger=logger, error=None, custom_message=f"FUNCTIONS SELECT: {x}", log_level="info")
        return x

    def select_one_for_primary(self, primary_key: int):
        """Selects a function by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE function_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_name(self, name: str):
        """Selects a function by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE function_name = "{name}"'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """Deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE function_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement methods for editing specific fields as needed
    def edit_function_description(self, new_description: str, primary_key: int):
        """Updates the function_description field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET function_description = "{new_description}" ' \
                f'WHERE function_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Add more methods for updating other fields as necessary
