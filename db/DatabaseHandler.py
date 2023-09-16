import mysql.connector


class DatabaseHandler:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = self.__connect()

    def create_database(self, database):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE {database}")
            cursor.close()
            self.connection.close()
            print("Database created successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def archive_database_to_a_file(self, file_name):
        try:
            cursor = self.connection.cursor()

            cursor.execute(
                f"SELECT * INTO OUTFILE '{file_name}' FROM {self.database}")
            cursor.close()
            self.connection.close()
            print("Database archived successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def load_database_from_a_file(self, file_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"LOAD DATA INFILE '{file_name}' INTO TABLE {self.database}")
            cursor.close()
            self.connection.close()
            print("Database loaded successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def __connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("Connected to the database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def __execute_query(self, query, data=None):
        try:
            cursor = self.connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            print("Query executed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

    def insert_data(self, table, data):
        query = f"INSERT INTO {table} VALUES ({', '.join(['%s'] * len(data))})"
        self.__execute_query(query, data)

    def delete_data(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.__execute_query(query)

    def update_data(self, table, update_values, condition):
        set_values = ', '.join([f"{key} = %s" for key in update_values.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        data = list(update_values.values())
        self.__execute_query(query, data)

    def archive_data(self, source_table, archive_table, condition):
        query = f"INSERT INTO {archive_table} SELECT * FROM {source_table} WHERE {condition}"
        self.__execute_query(query)

    def load_data(self, table):
        query = f"SELECT * FROM {table}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

# Example usage:
# db = DatabaseHandler("your_host", "your_user", "your_password", "your_database")
# db.connect()
# db.insert_data("your_table", ("John", "Doe"))
# db.update_data("your_table", {"first_name": "Jane"}, "last_name = 'Doe'")
# db.archive_data("your_table", "archive_table", "condition")
# data = db.load_data("your_table")
# print(data)
# db.close_connection()
