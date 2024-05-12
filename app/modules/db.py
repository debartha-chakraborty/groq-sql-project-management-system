from flask import Flask, jsonify, request
import psycopg2
import yaml
app = Flask(__name__)

# Load the database configuration from the config file
def get_config():
    with open('app\config.yaml', 'r') as f:
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


@app.route('/employees', methods=['GET'])
def get_employees():
    """Route to get all employees from the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    close_connection(conn)
    return jsonify(employees)


@app.route('/employee/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    """Route to get an employee by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee WHERE emp_id = %s", (id,))
    employee = cur.fetchone()
    close_connection(conn)
    if employee:
        return jsonify(employee)
    else:
        return jsonify({"error": "Employee not found"}), 404


@app.route('/employees', methods=['POST'])
def create_employee():
    """Route to create a new employee."""
    data = request.get_json()
    name = data.get('name')
    designation = data.get('designation')
    skills = data.get('skills')
    active_project_count = data.get('active_project_count')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO employee (name, designation, skills,  active_project_count) VALUES (%s, %s, %s, %s) RETURNING emp_id", (name, designation, skills,  active_project_count))
    new_employee_id = cur.fetchone()[0]
    conn.commit()
    close_connection(conn)
    return jsonify({"id": new_employee_id}), 201


@app.route('/employee/<int:id>', methods=['PUT'])
def update_employee(id):
    """Route to update an existing employee."""
    data = request.get_json()
    name = data.get('name')
    designation = data.get('designation')
    skills = data.get('skills')
    active_project_count = data.get('active_project_count')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE employee SET name = %s, designation = %s, skills = %s, active_project_count=%s WHERE emp_id = %s", (name, designation, skills,  active_project_count, id))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Employee updated successfully"})


@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """Route to delete an employee by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employee WHERE emp_id = %s", (id,))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Employee deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
