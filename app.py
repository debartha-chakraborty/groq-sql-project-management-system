from flask import Flask, jsonify, request
from modules.db import get_connection, close_connection

app = Flask(__name__)


@app.route('/')
def apis():
    text = """
    <h1>Employee Management API</h1>
    <p>Welcome to the Employee Management API! Here are the available endpoints:</p>
    <ul>
        <li>GET /get_employees - Get all employees</li>
        <li>GET /get_employees/{id} - Get an employee by ID</li>
        <li>POST /add_employee - Add a new employee</li>
        <li>PUT /update_employee_project_count/{id} - Update an employee's active project count</li>
        <li>DELETE /delete_employee/{id} - Delete an employee by ID</li>
    </ul>
    """
    return text


@app.route('/get_employees', methods=['GET'])
def get_employees():
    """Route to get all employees from the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    close_connection(conn)
    return jsonify(employees)


@app.route('/get_employees/<int:id>', methods=['GET'])
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


@app.route('/add_employee', methods=['POST'])
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


@app.route('/update_employee_project_count/<int:id>', methods=['PUT'])
def update_employee(id):
    """Route to update an existing employee."""
    data = request.get_json()
    id = data.get('id')
    active_project_count = data.get('active_project_count')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE employee SET active_project_count=%s WHERE emp_id = %s", (active_project_count, id))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Employee updated successfully"})


@app.route('/delete_employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """Route to delete an employee by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employee WHERE emp_id = %s", (id,))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Employee deleted successfully"})

# Add more routes and functions here, using db.get_connection()
# as needed for database access

if __name__ == '__main__':
    app.run(debug=True)
