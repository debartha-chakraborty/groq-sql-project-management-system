from flask import Flask, jsonify, request
from modules.db import get_connection, close_connection
from agents.main import ai_task_assigner
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


########################## DOCUMENTATION ROUTE ##########################
@app.route('/') #redirect to docs route
def home():
    return apis()

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
        <li>DELETE /delete_employee_batch - Delete multiple employees by ID - json body [id1,id2,id3, ...] </li>
    </ul>
    
    <h2>Task</h2>
    <ul>
        <li>GET /get_assigned_tasks - Get all tasks that is assigned</li>
        <li>GET /get_unassigned_tasks - Get all tasks that is not assigned</li>
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
    
    <h2>AI Agent</h2>
    <ul>
        <li>POST /ai_assign - Assign tasks to employees using AI agent</li>
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

@app.route('/delete_employee_batch', methods=['DELETE'])
def delete_employee_batch():
    """Route to delete multiple employees by ID."""
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    for id in data:
        cur.execute("DELETE FROM employee WHERE emp_id = %s", (id,))
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Employees deleted successfully with ids: " + str(data)})


########################## TASK ROUTES ##########################


@app.route('/get_assigned_tasks', methods=['GET'])
def get_assigned_tasks():
    """Route to get tasks which are assigned to any employee."""
    SQL = "SELECT * FROM task WHERE task_id IN (SELECT task_id FROM job)"
    
    conn = get_connection()
    cur = conn.cursor() 
    cur.execute(SQL)
    tasks = cur.fetchall()
    close_connection(conn)
    return jsonify(tasks)


@app.route('/get_unassigned_tasks', methods=['GET'])
def get_unassigned_tasks():
    """Route to get tasks which are not assigned to any employee."""
    SQL = "SELECT * FROM task WHERE task_id NOT IN (SELECT task_id FROM job)"
    
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
    cur.execute("SELECT e.name, e.designation, t.title, t.description, j.assignment_date, j.estimated_time, j.completion_date, j.status, j.task_id FROM job j JOIN employee e ON j.emp_id = e.emp_id JOIN task t ON j.task_id = t.task_id WHERE j.status != 'removed'")
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
    if new_job_id == None:
        conn.commit()
        close_connection(conn)
        return jsonify({"message": "Employee or Task not found"}), 404
    
    update_employee_project_count_sql = f"UPDATE employee SET active_project_count = active_project_count + 1 WHERE emp_id = {emp_id}"
    cur.execute(update_employee_project_count_sql)
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
        cur.execute(sql_query)
    elif status == 'completed':
        completion_date = datetime.now(timezone.utc)
        sql_query = f"UPDATE job SET {estimated_time_query}{character} status = '{status}', completion_date = '{completion_date}' WHERE task_id = {task_id}"    
        cur.execute(sql_query)
        active_project_count_sql = """
        UPDATE employee SET active_project_count = j.job_count FROM (SELECT emp_id, COUNT(*) AS job_count FROM job WHERE status NOT IN ('removed', 'completed') GROUP BY emp_id) AS j WHERE employee.emp_id = j.emp_id;
        UPDATE employee SET active_project_count = 0 WHERE emp_id NOT IN (SELECT emp_id FROM job WHERE status NOT IN ('removed', 'completed'));
        """
        cur.execute(active_project_count_sql)
    else:
        sql_query = f"UPDATE job SET {estimated_time_query}{character} status = '{status}' WHERE task_id = {task_id}"
        cur.execute(sql_query)
        active_project_count_sql = """
        UPDATE employee SET active_project_count = j.job_count FROM (SELECT emp_id, COUNT(*) AS job_count FROM job WHERE status NOT IN ('removed', 'completed') GROUP BY emp_id) AS j WHERE employee.emp_id = j.emp_id;
        UPDATE employee SET active_project_count = 0 WHERE emp_id NOT IN (SELECT emp_id FROM job WHERE status NOT IN ('removed', 'completed'));
        """
        cur.execute(active_project_count_sql)
    
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job updated successfully"})


@app.route('/remove_job/<int:task_id>', methods=['PUT'])
def remove_job(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE job SET status = 'removed' WHERE task_id = %s", (task_id, ))
    active_project_count_sql = """
    UPDATE employee SET active_project_count = j.job_count FROM (SELECT emp_id, COUNT(*) AS job_count FROM job WHERE status NOT IN ('removed', 'completed') GROUP BY emp_id) AS j WHERE employee.emp_id = j.emp_id;
    UPDATE employee SET active_project_count = 0 WHERE emp_id NOT IN (SELECT emp_id FROM job WHERE status NOT IN ('removed', 'completed'));
    """
    cur.execute(active_project_count_sql)
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job removed successfully"})


@app.route('/delete_job/<int:task_id>', methods=['DELETE'])
def delete_job(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM job WHERE task_id = %s", (task_id,))
    
    active_project_count_sql = """
    UPDATE employee SET active_project_count = j.job_count FROM (SELECT emp_id, COUNT(*) AS job_count FROM job WHERE status NOT IN ('removed', 'completed') GROUP BY emp_id) AS j WHERE employee.emp_id = j.emp_id;
    UPDATE employee SET active_project_count = 0 WHERE emp_id NOT IN (SELECT emp_id FROM job WHERE status NOT IN ('removed', 'completed'));
    """
    
    cur.execute(active_project_count_sql)
    
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Job deleted successfully"})



########################## AI Agent Utility APIs ##########################
 
@app.route('/ai_assign', methods=['POST'])
def ai_assign_task():
    """Route to assign employees and tasks with skills."""
    sql = ai_task_assigner()
    if sql == False:
        return jsonify({"message": "No tasks to assign"})
    if sql == "ERR":
        return jsonify({"error": "More Text generated by AI agent than expected"})
    
    print(sql)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    
    active_project_count_sql = """
    UPDATE employee SET active_project_count = j.job_count FROM (SELECT emp_id, COUNT(*) AS job_count FROM job WHERE status NOT IN ('removed', 'completed') GROUP BY emp_id) AS j WHERE employee.emp_id = j.emp_id;
    UPDATE employee SET active_project_count = 0 WHERE emp_id NOT IN (SELECT emp_id FROM job WHERE status NOT IN ('removed', 'completed'));
    """
    
    cur.execute(active_project_count_sql)
    
    
    conn.commit()
    close_connection(conn)
    return jsonify({"message": "Tasks assigned successfully"})
    

if __name__ == '__main__':
    app.run(debug=True)
