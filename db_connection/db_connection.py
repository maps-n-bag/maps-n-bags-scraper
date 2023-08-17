import psycopg2
import os
from en_variable.set_env import set_env
set_env()
def db_connection():
    try:
        conn=psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                port=os.getenv('DB_PORT'))
    except Exception as e:
        print(e)
    return conn