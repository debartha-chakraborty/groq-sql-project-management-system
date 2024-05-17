from textwrap import dedent
from crewai import Agent
from langchain_groq import ChatGroq


llm = ChatGroq(
		api_key="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",
		model="llama3-70b-8192",
		temperature=0
	)

def scrum_master_agent():
    	return Agent(
		role='Scrum Master',
		goal='Identify the time required to finish the provided tickets.',
		backstory=dedent("""You are a Scrum Master. You can provide estimate the required time to complete each ticket."""),
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
