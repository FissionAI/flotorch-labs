# Financial Document Analyzer (crewai-finagent)

crewai-finagent is an AI-powered application developed using FloTorch, a modern agent orchestration and experimentation framework. It leverages the CrewAI ecosystem to build multi-agent systems.

In this project, the goal is simple but powerful: take a financial PDF and turn it into structured, categorized, and insightful data — automatically. Three AI agents work together in sequence:

1.  **Extract Raw Transactions:** The first agent extracts the raw transaction data directly from the uploaded PDF.
2.  **Categorize Transactions:** The second agent intelligently categorizes these transactions by type (e.g., groceries, rent, entertainment).
3.  **Financial Analysis:** Finally, the third agent analyzes the categorized data to produce a concise summary of your financial habits and spending patterns.

## Installation

### Requirements

1.  Python 3.10+
2.  FloTorch Base URL and API key

### Setup

1.  **Clone the Repository**

    Open your terminal and run the following commands:

    ```bash
    git clone https://github.com/FissionAI/flotorch-labs.git
    cd finance/crewai-finance-agents/
    ```

2.  **Create and Activate a Virtual Environment**

    It's highly recommended to app/fd0f866a69d53a0fuse a virtual environment to manage project dependencies.

    ```bash
    # For Linux/macOS
    python -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**

    Navigate to the project directory and install the required Python packages:

    ```bash
    pip install -r src/financial_document_analyzer/requirements.txt
    ```

4.  **Set Up Environment Variables**

    You need to configure your FloTorch Base URL and API key. You can do this in a few ways:

    **Option 1: Exporting Environment Variables (for the current session)**

    ```bash
    # For Linux/macOS
    export OPENAI_BASE_URL=https://<gateway-url>/api/openai/v1
    export OPENAI_API_KEY=<secret-key>

    # For Windows
    set OPENAI_BASE_URL=https://<gateway-url>/api/openai/v1
    set OPENAI_API_KEY=<secret-key>
    ```

    **Option 2: Creating a `.env` File (recommended for persistent configuration)**

    Create a file named `.env` in the root of your project and add the following lines, replacing the placeholders with your actual values:

    ```
    OPENAI_BASE_URL=https://<gateway-url>/api/openai/v1
    OPENAI_API_KEY=<secret-key>
    ```

    **Note:** Using a `.env` file often requires an additional library to load these variables (though it's not strictly necessary for this setup if you access them using `os.environ`).


## Running the Project

To start your crew of AI agents and begin the financial document analysis, execute the following command from the root folder of your project:

```bash
python -m streamlit run src/financial_document_analyzer/streamlit_app/app.py
```
**Note:** Make sure you activate the virtual environment before running the streamlit run command.

You’ll be prompted to upload a financial PDF — for example, a bank or credit card statement.

## Understanding Your Crew

The financial_document_analyzer Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.
