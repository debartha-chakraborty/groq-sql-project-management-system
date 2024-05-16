from crewai import Crew
import json
from tasks import assignment_task
from my_agents import task_master_agent
from tools import get_empProjCount_task_details, get_empProjCount


def get_suited_employees():
	from tasks import identification_task
	from my_agents import senior_manager_agent
	from tools import get_employees_tasks_with_skills
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
	return output

def assign_task_availability(suited_employees_tasks):
    json_data = json.loads(suited_employees_tasks)
    # print(json_data)
    assignment_matrix = []
    for inner_list in json_data:
        print(inner_list)
        employees = inner_list[1]
        tasks = inner_list[0]
        # if more than one employee is suited for the task then get the project count for each employee and then assign the task to the employee with the least project count
        if len(employees) > 1:
            employees_details = get_empProjCount(employees)
            print(employees_details)
            #{5:2, 6:1, 7:3, ...}
            for task_id in tasks:
                #find the employee with the least project count		
                min_proj_count = min(employees_details.values())
                #get the employee_id with the least project count
                employee_id = [key for key in employees_details if employees_details[key] == min_proj_count][0]
                assignment_matrix.append((employee_id, task_id))
        else:
            for task_id in tasks:
                assignment_matrix.append((employee_id, task_id))
    return assignment_matrix
    
	

if __name__ == "__main__":
    suited_employees_tasks = get_suited_employees()
    assignment_matrix = assign_task_availability(suited_employees_tasks)
    print(assignment_matrix)
