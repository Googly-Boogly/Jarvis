import os

from global_code.helpful_functions import connect_to_db, create_logger_error, log_it

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='agents',
                             log_to_console=True, log_to_file=False)

class Agent:
    """
    Db class for the agents table.
    When creating new SQL queries, make sure to include spaces at the end of the line.
    """
    def __init__(self, data):
        self.table_name = 'agents'
        self.db = 'jarvis_db'

        self.agent_id = data.get('agent_id')  # Auto-increment field
        self.agent_name = data.get('agent_name')
        self.agent_description = data.get('agent_description')
        self.base_temp = data.get('base_temp')
        self.base_model = data.get('base_model')  # Foreign key to model_id in the models table
        self.long_term_memory = data.get('long_term_memory')
        self.contextual_environmental_memory = data.get('contextual_environmental_memory')
        self.task_delegation = data.get('task_delegation')
        self.emotional_intelligence = data.get('emotional_intelligence')

        self.added = data.get('added')  # Assuming added and updated times are handled by the database
        self.updated = data.get('updated')

    def save(self):
        """Saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(agent_name, agent_description, base_temp, base_model, long_term_memory, ' \
                f'contextual_environmental_memory, task_delegation, emotional_intelligence) ' \
                f'VALUES ("{self.agent_name}", "{self.agent_description}", {self.base_temp}, "{self.base_model}", ' \
                f'{self.long_term_memory}, {self.contextual_environmental_memory}, {self.task_delegation}, ' \
                f'{self.emotional_intelligence});'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """Selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        # log_it(logger=logger, error=None, custom_message=f"AGENTS SELECT: {x}", log_level="info")
        return x

    def select_one_for_primary(self, primary_key: int):
        """Selects an agent by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE agent_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_name(self, name: str):
        """Selects a model by its primary key"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE agent_name = "{name}"'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """Deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE agent_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Implement methods for editing specific fields as needed
    def edit_agent_description(self, new_description: str, primary_key: int):
        """Updates the agent_description field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET agent_description = "{new_description}" ' \
                f'WHERE agent_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    # Additional methods for updating other fields can be added here
