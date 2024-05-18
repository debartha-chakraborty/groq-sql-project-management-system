import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Establishes a connection to the Postgres database."""
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    # conn = psycopg2.connect(os.environ.get("DEMO_DATABASE_URL"))
    # conn = psycopg2.connect(os.environ.get("DEMO_TEST_DATABASE_URL"))
    return conn


def close_connection(conn):
    """Closes the connection to the database."""
    if conn:
        conn.close()


if __name__ == "__main__":
    conn = get_connection()
    close_connection(conn)
    print("Connection established successfully.")
