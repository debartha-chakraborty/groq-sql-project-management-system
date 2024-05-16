from crewai import Crew
import json
from .tools import get_all_empProjCount, get_empProjCount, get_task_details


def get_suited_employees():
    from .tasks import identification_task
    from .my_agents import senior_manager_agent
    from .tools import get_employees_tasks_with_skills
    # Create Agents
    senior_engineer_agent = senior_manager_agent()
    # Get employees and tasks
    employees, tasks = get_employees_tasks_with_skills()
    
    # Create Tasks
    identification_task = identification_task(senior_engineer_agent, employees, tasks)
    # Create Crew responsible for Copy
    crew = Crew(
		agents=[
			senior_engineer_agent
		],
		tasks=[
			identification_task
		],
		verbose=True
	)
    output = crew.kickoff()
    output = json.loads(output)
    return output

def assign_task_availability(suited_employees_tasks):
    assignment_matrix = []
    employees_project_count = get_all_empProjCount()
    for inner_list in suited_employees_tasks:
        employees = inner_list[1]
        tasks = inner_list[0]
        # if more than one employee is suited for the task then get the project count for each employee 
        # and then assign the task to the employee with the least project count
        if len(employees) == 1:
            for task_id in tasks:
                assignment_matrix.append([task_id, employees[0]])
                employees_project_count[employees[0]] += 1
        else:
            employees_details = get_empProjCount(employees)
            for task_id in tasks:
                employee_id = min(employees_details, key=employees_details.get)
                assignment_matrix.append([task_id, employee_id])
                employees_project_count[employee_id] += 1
                employees_details[employee_id] += 1
    return assignment_matrix


def get_estimated_time(assignment_matrix):
    from .tasks import assignment_task
    from .my_agents import scrum_master_agent
    
    task_ids = [task[0] for task in assignment_matrix]
    task_details = get_task_details(task_ids)
    
    crew = Crew(
		agents=[
			scrum_master_agent()
		],
		tasks=[
			assignment_task(scrum_master_agent(), assignment_matrix, task_details)
		],
		verbose=True
	)
    output = crew.kickoff()
    output = json.loads(output)
    return output

def join_task_details(assignment_matrix, task_details):
    # assignment_matrix Format [[task_id, employee_id], ...]
    # task_details Format [[task_id, estimated_time], ...]
    # Output target Format [(employee_id, task_id, estimated_time), ...]
    
    assign_mat_dict = {task[0]: task[1] for task in assignment_matrix}
    task_det_dict = {task[0]: task[1] for task in task_details}
    final_output = []
    for task_id, employee_id in assign_mat_dict.items():
        final_output.append((employee_id, task_id, task_det_dict[task_id]))
    return final_output

def build_sql_query(final_output):
    # INSERT INTO job (emp_id, task_id, estimated_time) VALUES (5, 2, 8), (3, 1, 4), (7, 4, 12);
	sql_query = "INSERT INTO job (emp_id, task_id, estimated_time) VALUES "
	values = str(final_output).replace("[", "").replace("]", "") + ";"
	return sql_query + values

def ai_task_assigner():
    suited_employees_tasks = get_suited_employees()
    assignment_matrix = assign_task_availability(suited_employees_tasks)
    task_details = get_estimated_time(assignment_matrix)
    final_output = join_task_details(assignment_matrix, task_details)
    sql = build_sql_query(final_output)
    return sql

if __name__ == "__main__":
    suited_employees_tasks = get_suited_employees()
    assignment_matrix = assign_task_availability(suited_employees_tasks)
    task_details = get_estimated_time(assignment_matrix)
    
    #DEBUG DATA
    # assignment_matrix = [[2, 5], [15, 5], [3, 3], [4, 5], [6, 1], [7, 7], [8, 5], [9, 10], [11, 10], [12, 2], [13, 5], [14, 5], [16, 10], [17, 1], [18, 2], [19, 5], [20, 3]]
    # task_details = [[2, 8], [3, 16], [4, 4], [6, 2], [7, 4], [8, 12], [9, 2], [11, 4], [12, 8], [13, 40], [14, 12], [15, 16], [16, 8], [17, 8], [18, 2], [19, 8], [20, 24]]
    ##EXPECTED OUTPUT
    # [(5, 2, 8), (5, 15, 16), (3, 3, 16), (5, 4, 4), (1, 6, 2), (7, 7, 4), (5, 8, 12), (10, 9, 2), (10, 11, 4), (2, 12, 8), (5, 13, 40), (5, 14, 12), (10, 16, 8), (1, 17, 8), (2, 18, 2), (5, 19, 8), (3, 20, 24)]
    final_output = join_task_details(assignment_matrix, task_details)
    sql = build_sql_query(final_output)
    
    # print(suited_employees_tasks)
    # print(assignment_matrix)
    # print(task_details)
    # print(final_output)
    # print(sql)
    
