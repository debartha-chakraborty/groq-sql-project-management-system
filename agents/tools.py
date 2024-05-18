from .db import get_connection, close_connection
from crewai_tools import tool


def get_employees_tasks_with_skills():
    """Returns the employees and tasks with their skills."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.emp_id, e.skills FROM employee e")
    employees = cur.fetchall()
    cur.execute("SELECT task_id, ideal_skills FROM task  WHERE task_id NOT IN (SELECT task_id FROM job)")
    tasks = cur.fetchall()
    close_connection(conn)
    return employees, tasks

def get_all_empProjCount():
    """Returns the project count for all employees."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.emp_id, e.active_project_count FROM employee e")
    employees = cur.fetchall()
    close_connection(conn)
    
    employees = {emp[0]: emp[1] for emp in employees}
    return employees

def get_empProjCount(employee_list):
    """Returns the project count for each employee.""" 
    if employee_list == []:
        return {"error": "The Input list is empty."}
    employee_list = tuple(employee_list)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.emp_id, e.active_project_count FROM employee e WHERE e.emp_id IN %s", (employee_list,))
    employees = cur.fetchall()
    close_connection(conn)
    
    #convert it to a dictionary with emp_id as key
    employees = {emp[0]: emp[1] for emp in employees}
    return employees

def get_task_details(task_list):
    """Returns the task details."""
    task_list = tuple(task_list)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT t.task_id, t.title, t.description FROM task t WHERE t.task_id IN %s", (task_list,))
    tasks = cur.fetchall()
    close_connection(conn)
    return tasks

# @tool("employee project count tool")
def get_empProjCount_task_details(task_employee_list):
    """Returns the project count for each employee and the task details."""
    tasks = task_employee_list[0] #[task_id1, task_id2, ...]
    employees = task_employee_list[1] #[employee_id1, employee_id2, ...]
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get the project count for each employee
    cur.execute("SELECT e.emp_id, e.active_project_count FROM employee e WHERE e.emp_id IN %s", (employees,))
    employees = cur.fetchall()
    
    # Get the task details
    cur.execute("SELECT t.task_id, t.title, t.description FROM task t WHERE t.task_id IN %s", (tasks,))
    tasks = cur.fetchall()
    
    close_connection(conn)
    return employees, tasks

@tool("assign task tool")
def assign_task(emp_task_time_list):
    """Assigns tasks to employees with estimated time to complete the task."""
    for emp_task_time in emp_task_time_list:
        emp_id = emp_task_time[0]
        task_id = emp_task_time[1]
        estimated_time = emp_task_time[2]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO job (emp_id, task_id, estimated_time) VALUES (%s, %s, %s) RETURNING (emp_id, task_id)", (emp_id, task_id, estimated_time))
        close_connection(conn)
        
    return "Task assigned successfully"


if __name__ == "__main__":
    employees, tasks =get_employees_tasks_with_skills()
    print(employees)
    print(tasks)
    # print(get_empProjCount_task_details([["task_id1", "task_id2"], ["employee_id1", "employee_id2"]]))
    # print(assign_task([["employee_id1", "task_id1", 10], ["employee_id2", "task_id2", 20]]))