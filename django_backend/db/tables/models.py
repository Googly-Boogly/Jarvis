import os

from global_code.helpful_functions import connect_to_db, create_logger_error, log_it

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='models',
                             log_to_console=True, log_to_file=False)

class Model:
    """
    Db class for the models table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'models'
        self.db = 'jarvis_db'

        self.model_id = data.get('model_id')  # Auto-increment field
        self.model_name = data.get('model_name')
        self.company = data.get('company')
        self.model_info = data.get('model_info')
        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')

    def save(self):
        """Saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(model_name, company, model_info) ' \
                f'VALUES ("{self.model_name}", "{self.company}", "{self.model_info}");'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """Selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        # log_it(logger=logger, error=None, custom_message=f"MODELS SELECT: {x}", log_level="info")
        return x

    def select_one_for_primary(self, primary_key: int):
        """Selects a model by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE model_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_name(self, name: str):
        """Selects a model by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE model_name = "{name}"'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """Deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE model_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement other specific field editing methods as needed
    def edit_model_info(self, new_model_info: str, primary_key: int):
        """Updates the model_info field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET model_info = "{new_model_info}" ' \
                f'WHERE model_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Add more methods for editing other fields as necessary
