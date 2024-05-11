from flask import Flask
from .modules import db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


# Add more routes and functions here, using db.get_connection()
# as needed for database access

if __name__ == '__main__':
    app.run(debug=True)
