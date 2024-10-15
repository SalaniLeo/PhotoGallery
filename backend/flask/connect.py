import psycopg2
from config import load_config

config = load_config()

print(config)

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
def get_db_connection(cursor_factory=None):
    conn = psycopg2.connect(config)
    cur = conn.cursor(cursor_factory)
    return cur, conn