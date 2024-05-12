from flask import jsonify, request
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

