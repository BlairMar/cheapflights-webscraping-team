import psycopg2

from db_secrets import USERNAME, PASSWORD

class DatabaseConnection:
    """
    DatabaseConnection: Class
    
    Class to avoid rewriting boilerplate code for creating connections to a Postgres database.
    Will be used in a context manager in other parts of the code.
    """

    def __init__(self, host):
        """
        Initialiser for database Connection Boilerplate.

        Parameters
        ----------
        host : str
            host is the host address for the database. 
            Currently set as localhost for now, kept as a var instead of a default argument
            incase it changes (AWS).
        """
        self.connection = None
        self.host = host
        
    def enter(self):
        """
        Boilerplate for creating a new database connection.
        """
        self.connection = psycopg2.connect(
            host=self.host, 
            dbname="Cheapflights-Scraper",
            username=USERNAME,
            password=PASSWORD
        )
    
    def exit(self):
        """
        Boilerplate for closing a database connection after commiting any pending transactions.
        """
        self.connection.commit()
        self.connection.close()