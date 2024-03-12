import os

from global_code.helpful_functions import connect_to_db


class WebsiteState:
    """
    Db class for the website_state table.
    Handles interactions with the website's state records.
    """
    def __init__(self, data):
        self.table_name = 'website_state'
        self.db = 'jarvis_db'

        self.website_state_id = data.get('website_state_id')
        self.user_id = data.get('user_id')
        self.tts = data.get('tts')
        self.stt = data.get('stt')
        self.current_chat = data.get('current_chat')
        self.model_selected = data.get('model_selected')
        self.temperature = data.get('temperature')
        self.agent_selected = data.get('agent_selected')

    def save(self):
        """Saves one instance to the table."""
        query = f'INSERT INTO {self.table_name} ' \
                f'(user_id, tts, stt, current_chat, model_selected, temperature, agent_selected) ' \
                f'VALUES ({self.user_id}, {self.tts}, {self.stt}, {self.current_chat}, ' \
                f'"{self.model_selected}", {self.temperature}, "{self.agent_selected}");'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """Selects all records from the table."""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_primary(self, primary_key: int):
        """Selects a record by its primary key."""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE website_state_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """Deletes one instance from the table."""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE website_state_id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def edit_any_row(self, new_name: str, primary_key: int, row_name: str):
        """Updates the name field of a record given its primary key"""
        query = f'UPDATE {self.table_name} ' \
                f'SET {row_name} = "{new_name}" ' \
                f'WHERE user_id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x
    # Implement edit methods as needed
