#%%

from db_conn import DatabaseConnection

def create_db(db_name):
    with DatabaseConnection('cheapflights-db.clc2fxqcvl9j.eu-west-2.rds.amazonaws.com') as conn:
        conn.execute(f'DROP DATABASE {db_name}')
        


def create_table(table_name):
    with DatabaseConnection('cheapflights-db.clc2fxqcvl9j.eu-west-2.rds.amazonaws.com') as conn:
        conn.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(city_id INTEGER PRIMARY KEY')
    
create_db('test')
# %%
