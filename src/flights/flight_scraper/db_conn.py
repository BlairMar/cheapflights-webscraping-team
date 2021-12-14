import psycopg2
from db_secrets import USERNAME, PASSWORD

class DatabaseConnection:
    """
    DatabaseConnection: Class

    Class to avoid rewriting boilerplate code
    for creating connections to a Postgres database.
    Will be used in a context manager in other parts of the code.
    """

    def __init__(self, host):
        """
        Initialiser for database Connection Boilerplate.

        Parameters
        ----------
        host : str
            host is the host address for the database.
            Currently set as localhost for now, kept as a var
            instead of a default argument
            incase it changes (AWS).
        """
        self.host = host
        self.connection = None

    def __enter__(self):
        """
        Boilerplate for creating a new database connection.
        Initialises the cursor inside context manager,
        cursor methods called outside.

        e.g:
        with DatabaseConnection('localhost') as connection:
            try:
                connection.execute() 'instead of connection.cursor.execute()'
            except psycopg2.Error as e:
                print(e.pgerror)

        """
        self.connection = psycopg2.connect(
            host=self.host,
            port="5432",
            user=USERNAME,
            password=PASSWORD,
        )
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        return cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Boilerplate for closing a database connection after
        commiting any pending transactions.
        If any exceptions are raised,
        connection is immediately closed without committing.
        """
        if exc_type or exc_value or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
