from db_conn import DatabaseConnection
from db_secrets import RDS_INSTANCE

def create_schema():
    with DatabaseConnection() as conn:
        pass