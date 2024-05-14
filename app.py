from flask import Flask, jsonify, request
from modules.db import get_connection, close_connection
from datetime import date, datetime, timedelta, timezone
from flask_cors import CORS
app = Flask(__name__)


CORS(app) # This will enable CORS for all routes

# Adding CORS headers to the response
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response




@app.route('/docs')
def apis():
    text = """
    <h1>Employee Management API</h1>
    <p>Welcome to the Employee Management API! Here are the available endpoints:</p>
    <h2>Employee</h2>
    <ul>
        <li>GET /get_employees - Get all employees</li>
        <li>GET /get_employees/{id} - Get an employee by ID</li>
        <li>POST /add_employee - Add a new employee</li>
        <li>PUT /update_employee_project_count/{id} - Update an employee's active project count</li>
        <li>DELETE /delete_employee/{id} - Delete an employee by ID</li>
    </ul>
    
    <h2>Task</h2>
    <ul>
        <li>GET /get_tasks - Get all tasks within the last 28 days</li>
        <li>GET /get_tasks?start={start_date} - Get tasks from start date to present</li>
        <li>GET /get_tasks?start={start_date}&end={end_date} - Get tasks within the specified date range</li>
        <li>POST /add_task - Add a new task</li>
        <li>PUT /update_task/{task_id} - Update a task by ID</li>
        <li>DELETE /delete_task/{task_id} - Delete a task by ID</li>        
    </ul>
    
    <h2>Job</h2>
    <ul>
        <li>GET /get_jobs - Get all jobs</li>
        <li>POST /add_job - Add a new job</li>
        <li>PUT /update_job/{task_id} - Update a job by task ID</li>
        <li>PUT /remove_job/{task_id} - Remove a job by task ID</li>
        <li>DELETE /delete_job/{task_id} - Delete a job by task ID</li>
    </ul>
    """
    return text

########################## EMPLOYEE ROUTES ##########################


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


########################## TASK ROUTES ##########################

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    """Route to get tasks within the last 28 days or within the specified date range."""
   
    start_date = request.args.get('start')
    end_date = request.args.get('end') 
    curr_date = date.today()
    
    if start_date == None:
        start_date = curr_date - timedelta(days=28)
        SQL = f"SELECT * FROM task WHERE request_date > '{start_date}'"
    else:
        if end_date == None:
            SQL = f"SELECT * FROM task WHERE request_date > '{start_date}'"
        else:
            SQL = f"SELECT * FROM task WHERE request_date BETWEEN '{start_date}' AND '{end_date}'"
            
        
    conn = get_connection()
    cur = conn.cursor() 
    cur.execute(SQL)
    tasks = cur.fetchall()
    close_connection(conn)
    return jsonify(tasks)




@app.route('/add_task', methods=['POST'])
def add_task():
    """Route to add a new task."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    request_date = datetime.now(timezone.utc)
    tech = data.get('tech')
    ideal_skills = data.get('ideal_skills')
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO task (title, description, request_date, tech, ideal_skills) VALUES (%s, %s, %s, %s, %s) RETURNING task_id", (title, description, request_date, tech, ideal_skills))
    new_task_id = cur.fetchone()[0]
    conn.commit()
    close_connection(conn)
    return jsonify({"task_id": new_task_id}), 201


@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Route to update an existing task."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tech = data.get('tech')
    ideal_skills = data.get('ideal_skills')
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE task SET title = %s, description = %s, tech = %s, ideal_skills = %s WHERE task_id = %s", (title, description, tech, ideal_skills, task_id))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Task updated successfully"})


@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Route to delete a task by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM task WHERE task_id = %s", (task_id,))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Task deleted successfully"})


########################## JOB ROUTES ##########################

@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.name, e.designation, t.title, t.description, j.assignment_date, j.estimated_time, j.completion_date, j.status FROM job j JOIN employee e ON j.emp_id = e.emp_id JOIN task t ON j.task_id = t.task_id WHERE j.status != 'removed'")
    jobs = cur.fetchall()
    close_connection(conn)
    return jsonify(jobs)

@app.route('/add_job', methods=['POST'])
def add_job():
    data = request.get_json()
    emp_id = data.get('emp_id')
    task_id = data.get('task_id')
    estimated_time = data.get('estimated_time')
    assignment_date = datetime.now(timezone.utc)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO job (emp_id, task_id, estimated_time, assignment_date) VALUES (%s, %s, %s, %s) RETURNING (emp_id, task_id)", (emp_id, task_id, estimated_time, assignment_date))
    new_job_id = cur.fetchone()[0]
    conn.commit()
    close_connection(conn)
    return jsonify({"job_id": new_job_id}), 201

@app.route('/update_job/<int:task_id>', methods=['PUT'])
def update_job(task_id):
    data = request.get_json()
    estimated_time = data.get('estimated_time')
    status = data.get('status')
    conn = get_connection()
    cur = conn.cursor()
    if estimated_time == None:
        estimated_time_query = ''
    else:
        estimated_time_query = f"estimated_time = {estimated_time} "
    character = '' if estimated_time_query == '' else ','
    if status == None:
        sql_query = f"UPDATE job SET {estimated_time_query} WHERE task_id = {task_id}"
    elif status == 'completed':
        completion_date = datetime.now(timezone.utc)
        sql_query = f"UPDATE job SET {estimated_time_query}{character} status = '{status}', completion_date = '{completion_date}' WHERE task_id = {task_id}"    
    else:
        sql_query = f"UPDATE job SET {estimated_time_query}{character} status = '{status}' WHERE task_id = {task_id}"
    # print(f"\n\n{sql_query}\n\n")
    cur.execute(sql_query)
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job updated successfully"})


@app.route('/remove_job/<int:task_id>', methods=['PUT'])
def remove_job(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE job SET status = 'removed' WHERE task_id = %s", (task_id, ))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job removed successfully"})


@app.route('/delete_job/<int:task_id>', methods=['DELETE'])
def delete_job(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM job WHERE task_id = %s", (task_id,))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job deleted successfully"})
 

if __name__ == '__main__':
    app.run(debug=True)
