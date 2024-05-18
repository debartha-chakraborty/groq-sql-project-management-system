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
        expected_output="""example: [[[ticket_id1, ticket_id2, ...], [employee_id1, employee_id2, ...]] , [[ticket_id3], [employee_id3,]]] 
        You can only use employee_id and ticket_id from the given tables. Do not make imaginary employee_id. 
		If you do not have any matching skills for a ticket, suggest it to the employees with the closest matching skill. Do no explain the reasoning behind the time estimation.
		""",
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
