import psycopg2
import os
from en_variable.set_env import set_env
set_env()
def db_connection():
    try:
        conn=psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DBNAME'),
                user=os.getenv('PGUSER'),
                password=os.getenv('PGPASSWORD'),
                port=os.getenv('PORT'))
    except Exception as e:
        print(e)
    return conn