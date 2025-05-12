# Floagentdemo Crew

Welcome to the Floagentdemo Crew project, powered by [crewAI](https://crewai.com). This is a simple agentic workflow of a financial agent. The crew takes pdf as input and outputs a detailed finanacial analysis report

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Setup

**Rename `.env.example` to `.env` and add Flotorch Gateway Key as  `OPENAI_API_KEY`**

- Modify `src/floagentdemo/config/agents.yaml` to define your agents
- Modify `src/floagentdemo/config/tasks.yaml` to define your tasks
- Modify `src/floagentdemo/crew.py` to add your own logic, tools and specific args
- Modify `src/floagentdemo/main.py` to add custom inputs for your agents and tasks
- Modify `src/floagentdemo/api.py` to add your own logic, tools and specific args

If you are using a different FloTorch Gateway, you can modify the `OPENAI_API_BASE` in the `.env` file. by default it is set to `https://fphcciizk3.us-east-1.awsapprunner.com/api/v1`

## Running the CrewAI Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the floagentdemo Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

**Note:** Make sure you activate the virtual environment before running the crewai run command.

## Running the api

```bash
uvicorn src.floagentdemo.api:app
```

The api server should be running on `http://127.0.0.1:8000`

**Note:** Make sure you activate the virtual environment before running the api server.

## Troubleshooting

If your env variables are not being loaded, you can try to run the following command:

```bash
OPENAI_API_BASE="https://fphcciizk3.us-east-1.awsapprunner.com/api/v1" OPENAI_API_KEY="your-api-key" uvicorn src.floagentdemo.api:app
```



## Understanding Your Crew

The floagentdemo Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.
