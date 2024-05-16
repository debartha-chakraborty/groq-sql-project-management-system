from textwrap import dedent
from crewai import Agent
from langchain_groq import ChatGroq


llm = ChatGroq(
		api_key="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",
		model="llama3-70b-8192",
		temperature=0
	)

def task_master_agent():
    	return Agent(
		role='Task Master',
		goal='Assign new ticket to the most suitable employee based on employee availability.',
		backstory=dedent("""You are a Task Master. Your job is to assign new ticket to the most suitable employee. You also add the estimated time to complete for each ticket."""),
		allow_delegation=False,
		llm=llm,
		verbose=True
	)

def senior_manager_agent():
	return Agent(
		role='Senior Project Manager',
		goal='Identify similar skilled employees and similar tickets to assign based on employee skillset and ticket requirements',
		backstory=dedent("""You are a Project Manager. Your job is to identify tickets and the suitable employees."""),
		allow_delegation=False,
		llm=llm,
		verbose=True
		)
