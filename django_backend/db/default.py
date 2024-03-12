"""
THIS IS JUST A SAMPLE PAGE DO NOT ACTUALLY CALL THIS PAGE
when creating a new sql table class copy and paste this page and change the class name to the table name
"""
import os

from global_code.helpful_functions import connect_to_db


class CHANGEME:
    """
    Db class
    When creating new sql queries, make sure to use include spaces at the end of the line
    """
    def __init__(self, data):
        self.table_name = 'CHANGEME'
        self.db = 'jarvis_db'

        if 'id' in data:
            self.id: str = data['id']
        if 'pw' in data:
            self.pw: str = data['pw']
        if 'email_address' in data:
            self.email_address: str = data['email_address']

    def save(self):
        """saves one instance to the table"""
        query = f'INSERT INTO {self.table_name} ' \
                f'(changeme) ' \
                f'VALUES (changeme);'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_all(self):
        """selects all from table"""
        query = f'SELECT * FROM {self.table_name}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def select_one_for_primary(self, primary_key: int):
        """selects all from table"""
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def delete(self, primary_key: int):
        """deletes one instance from the table"""
        query = f'DELETE FROM {self.table_name} ' \
                f'WHERE id = {primary_key}'

        x = connect_to_db(self.db).query_db(query)
        return x

    def edit_all(self, primary_key: int):
        """Will edit all the fields of the table given id"""
        raise NotImplemented
        query = f'UPDATE {self.table_name} ' \
                f'SET changeme = {self.changeme} ' \
                f'WHERE id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

    def edit_specific_field(self, field_name: str, field_value: str, primary_key: int):
        """Will edit a specific field of the table given id"""
        query = f'UPDATE {self.table_name} ' \
                f'SET {field_name} = {field_value} ' \
                f'WHERE id = {primary_key};'

        x = connect_to_db(self.db).query_db(query)
        return x

