import psycopg2
import yaml

# Load the database configuration from the config file
def get_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)['database']
    return config


def get_connection():
    """Establishes a connection to the Postgres database."""
    params = get_config()
    conn = psycopg2.connect(**params)
    return conn


def close_connection(conn):
    """Closes the connection to the database."""
    if conn:
        conn.close()



if __name__ == '__main__':
    conn = get_connection()
    print(conn)
    
    SELECT_QUERY_1 = "SELECT * FROM employee;"
    SELECT_QUERY_2 = "SELECT * FROM task;"
    SELECT_QUERY_3 = "SELECT * FROM job;"
    
    # Create a cursor object
    cur = conn.cursor()
    # Execute the SELECT query
    cur.execute(SELECT_QUERY_1)
    print(cur.fetchall())
    
    cur.execute(SELECT_QUERY_2)
    print(cur.fetchall())
    
    cur.execute(SELECT_QUERY_3)
    print(cur.fetchall())
    
    close_connection(conn)