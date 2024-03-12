import os

from global_code.helpful_functions import connect_to_db, create_logger_error, log_it

logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='agent_functions',
                             log_to_console=True, log_to_file=False)

class AgentFunctions:
    """
    Db class for the agent_functions linking table.
    This class manages the many-to-many relationship between agents and functions.
    """
    def __init__(self, db='jarvis_db'):
        self.table_name = 'agent_functions'
        self.db = db

    def link_agent_to_function(self, agent_id: int, function_id: int):
        """Links an agent to a function by inserting a record into the agent_functions table."""
        query = f'INSERT INTO {self.table_name} (agent_id, function_id) ' \
                f'VALUES ({agent_id}, {function_id});'

        x = connect_to_db(self.db).query_db(query)
        return x

    def unlink_agent_from_function(self, agent_id: int, function_id: int):
        """Unlinks an agent from a function by deleting a record from the agent_functions table."""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE agent_id = {agent_id} AND function_id = {function_id};'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_functions_for_agent(self, agent_id: int):
        """Selects all functions linked to a specific agent."""
        query = f'SELECT function_id FROM {self.table_name} ' \
                f'WHERE agent_id = {agent_id};'

        x = connect_to_db(self.db).query_db(query)

        return x

    def select_agents_for_function(self, function_id: int):
        """Selects all agents linked to a specific function."""
        query = f'SELECT agent_id FROM {self.table_name} ' \
                f'WHERE function_id = {function_id};'

        x = connect_to_db(self.db).query_db(query)

        return x

    def select_all(self):
        """Selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x
    # Additional methods for managing agent-function relationships can be added here
