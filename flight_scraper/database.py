import psycopg2


from db_conn import DatabaseConnection


"""
Module containing helper functions for creating schemas and tables in DB,
as well as methods for inserting or querying data from the tables
"""


def create_schema(schema: str) -> None:
    """
    create_schema [summary]

    Parameters
    ----------
    schema : str
        [description]
    """
    with DatabaseConnection("localhost") as connection:
        try:
            connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        except psycopg2.Error as e:
            print(e.pgerror)


def create_table(table: str) -> None:
    """
    create_table [summary]

    Parameters
    ----------
    table : str
        [description]
    """
    with DatabaseConnection("localhost") as connection:
        try:
            connection.execute(f"CREATE TABLE IF NOT EXISTS {table}")
        except psycopg2.Error as e:
            print(e.pgerror)


def drop_table(table: str) -> None:
    """
    drop_table [summary]

    Parameters
    ----------
    table : str
        [description]
    """
    with DatabaseConnection("localhost") as connection:
        try:
            connection.execute(f"DROP TABLE IF EXISTS {table}")
        except psycopg2.Error as e:
            print(e.pgerror)

create_schema('Destinations')