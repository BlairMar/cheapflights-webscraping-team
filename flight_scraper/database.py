from .db_conn import DatabaseConnection


"""
Helper functions for creating table in DB, 
as well as methods for inserting or querying data from the tables
"""
def create_flights_table():
    with DatabaseConnection as connection:
        cursor = connection.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS flights(")