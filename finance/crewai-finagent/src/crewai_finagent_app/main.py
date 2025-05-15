#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_finagent_app.crew import Floagentdemo

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    """ Read text from file"""
    with open('src/crewai_finagent_app/data/statement.txt', 'r') as file:
        contents = file.read()
    inputs = {
        'statement_text': contents,
    }
    
    try:
        Floagentdemo().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    with open('src/crewai_finagent_app/data/statement.txt', 'r') as file:
        contents = file.read()
    inputs = {
        'statement_text': contents,
    }
    try:
        Floagentdemo().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Floagentdemo().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    with open('src/crewai_finagent_app/data/statement.txt', 'r') as file:
        contents = file.read()
    inputs = {
        'statement_text': contents,
    }
    try:
        Floagentdemo().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
