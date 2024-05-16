from textwrap import dedent
from crewai import Task


def identification_task(agent, employees, tickets):
	return Task(description=dedent(
		f"""
		You will identify the most suitable employees for tickets based on the employee's skillsets and the ticket's skill requirements. Tickets are the priorit
		All the tickets must be assigned to an employee. All employees are not required to be assigned a task. No duplicates are allowed in the final answer.
		employees Format: [employee_id, skillset]
		tickets Format: [ticket_id, skill_requirements]

		Employee Table
		--------------
		{employees}

		Ticket Table
		------------
		{tickets}
		"""
		),
        expected_output="example: [[[ticket_id1, ticket_id2, ...], [employee_id1, employee_id2, ...]] , [[ticket_id3], [employee_id3,]]] \
		where ticket_id1, ticket_id2, ticket_id3 are the ticket ids and employee_id1, employee_id2, employee_id3 are the employee ids. \
		ticket_id1 and ticket_id2 are similar and employee_id1 and employee_id2 are similar. ticket_id3 and employee_id3 are similar.Your Final answer must be in the format [[[ticket_id1, ticket_id2, ...], [employee_id1, employee_id2, ...]], ...]",
		agent=agent
	)
		
def assignment_task(agent, employee, task):
	return Task(description=dedent(
		f"""You will estimate the time required in hours for the task based on task description and title.

		Task
		----
		{task}
  
		"""),
		expected_output="You will look over the ticket and format it in the format [[task_id, estimated_time_in_hours], ...] Your Final answer must be the ticket and estimated time only, the ticket and nothing else.",
		agent=agent
	)
