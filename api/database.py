import psycopg2
from psycopg2 import Error


class Database:
    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
            )
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error: {e}")
            return None

    def insert_data(self, table_name, columns, values):
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        self.execute_query(query, values)

    def select_data(self, table_name, columns="*", condition=None):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)

    def update_data(self, table_name, set_values, condition=None):
        query = f"UPDATE {table_name} SET {set_values}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query)

    def delete_data(self, table_name, condition=None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query)
