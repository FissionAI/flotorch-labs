# Financial Document Analyzer(crewai-finagent)

crewai-finagent is an AI-powered application developed using FloTorch, a modern agent orchestration and experimentation framework. It leverages the CrewAI ecosystem to build multi-agent LLM workflows where specialized agents collaborate to complete a task.

In this case, the goal is simple but powerful: take a financial PDF, and turn it into structured, categorized, and insightful data — automatically.
In this project, three AI agents work together in sequence.
    1. Extract raw transactions from a PDF.
    2. Categorize those transactions by type (e.g., groceries, rent).
    3. Analyze the data to produce a summary of your financial habits

## Installation
Requirements:
    Python 3.10+
    FloTorch Base URL and  API key

### Setup
1. Clone the repository
	Run this in your terminal
	-> git clone https://github.com/FissionAI/flotorch-labs.git
	-> cd finance/finance-document-analyzer/

2. Create and activate a virtual environment
	-> python -m venv venv
    -> source venv/bin/activate (For Linux/macOS)
    -> venv\Scripts\activate(For Windows)

3. Install dependencies
	-> pip install -r requirements.txt

4. Set up environment variables
	(For Linux/macOS)
	-> export OPENAI_BASE_URL=https://<gateway-url>/api/openai/v1
	-> export OPENAI_API_KEY=<secret-key>
	(For Windows)
	-> set OPENAI_BASE_URL=https://<gateway-url>/api/openai/v1
	-> set OPENAI_API_KEY=<secret-key>
	
# Refer this flotorch-documentation for instructions on creating a FloTorch gateway and generating an API key.

## Running the Project
To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:
RUN python -m streamlit run src/floagentdemo/streamlitDemo/app.py

**Note:** Make sure you activate the virtual environment before running the crewai run command.

You’ll be prompted to upload a financial PDF — for example, a bank or credit card statement.

## Understanding Your Crew

The floagentdemo Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.
