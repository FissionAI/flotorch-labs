import traceback

import pypdf
import json
import re
from src.financial_document_analyzer.crew import Floagentdemo
import pandas as pd


def complete_json(json_string):
    try:
        # Attempt to parse JSON
        data = json.loads(json_string)
    except json.JSONDecodeError:
        # Handle incomplete JSON by removing the last unclosed element
        json_string = json_string.strip()
        last_open_brace = json_string.rfind("{")
        json_string = json_string[:last_open_brace]  # Remove the last unclosed object
        json_string = re.sub(r',\s*$', '', json_string)  # Remove trailing comma if any
        json_string += "\n]"  # Close the JSON array properly
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError:
            raise ValueError("JSON is incomplete or malformed")
    return data

def clean_json_output(llm_output):
    try:
        if isinstance(llm_output, str):
            # Remove optional triple quotes or backticks if present
            cleaned_output = re.sub(r"^```json\s*|\s*```$", "", llm_output.strip(), flags=re.MULTILINE)
            # Remove any leading 'json' keyword (if exists)
            cleaned_output = re.sub(r"^json\s*", "", cleaned_output.strip(), flags=re.IGNORECASE)
            return json.loads(cleaned_output)
        else:
            json_string = json.dumps(llm_output)
            return json.loads(json_string)
    except json.JSONDecodeError as e:
        # Attempt to fix common issues like trailing commas or unescaped characters
        cleaned_output = llm_output.strip()

        # Remove trailing commas within curly braces and square brackets
        cleaned_output = re.sub(r',\s*}', '}', cleaned_output)
        cleaned_output = re.sub(r',\s*]', ']', cleaned_output)

        # Attempt to handle unescaped single quotes by replacing them with double quotes
        # This is a risky operation and might break valid JSON. Use with caution.
        cleaned_output = cleaned_output.replace("'", '"')

        try:
            return json.loads(cleaned_output)
        except json.JSONDecodeError as e2:
            raise ValueError(f"LLM output is not valid JSON even after cleaning: Original error: {e}, Cleaning error: {e2}, Output: {llm_output}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")

def serialize_crew_output(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, (list, tuple)):
        return [serialize_crew_output(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_crew_output(value) for key, value in obj.items()}
    else:
        return str(obj)

def update_analysis(task3_response, task2_response):
    """
    Updates the analysis results with summary statistics, spending distribution,
    and monthly spending trends.

    Args:
        task3_response (dict): The analysis result dictionary.
        task2_response (list): The list of categorized transactions.

    Returns:
        dict: The updated task3_response dictionary.
    """

    df = pd.DataFrame(task2_response)

    # Calculate summary statistics
    update_summary_statistics(task3_response, df)

    # Calculate spending distribution
    update_spending_distribution(task3_response, df)

    # Calculate monthly spending trends
    update_monthly_spending(task3_response, df)

    return task3_response

def update_summary_statistics(task3_response, df):
    """Updates summary statistics in the task3_response."""
    total_income = df[df['type'] == 'credit']['amount'].sum()
    total_expenses = df[df['type'] == 'debit']['amount'].sum()
    task3_response['summary_statistics']['total_income'] = round(total_income, 2)
    task3_response['summary_statistics']['total_expenses'] = round(total_expenses, 2)
    task3_response['summary_statistics']['net_income'] = round(total_income - total_expenses, 2)

def update_spending_distribution(task3_response, df):
    """Updates spending distribution and top spending categories."""
    debit_df = df[df['type'] == 'debit']
    spending_data = debit_df.groupby('category')['amount'].sum().reset_index()
    total_spending = spending_data['amount'].sum()

    if total_spending == 0:
        task3_response['category_analysis']['spending_distribution'] = []
        task3_response['category_analysis']['top_spending_categories'] = []
        return

    spending_data['percentage'] = (spending_data['amount'] / total_spending) * 100
    spending_data['percentage'] = round(spending_data['percentage'], 2)
    spending_data['amount'] = round(spending_data['amount'], 2)

    # Adjust percentages to sum to 100%
    diff = 100 - spending_data['percentage'].sum()
    if abs(diff) > 1e-9: #avoid floating point errors.
        adjust_percentages(spending_data, diff)

    task3_response['category_analysis']['spending_distribution'] = spending_data.to_dict(orient='records')
    task3_response['category_analysis']['top_spending_categories'] = spending_data.nlargest(3, 'amount').to_dict(orient='records')

def adjust_percentages(spending_data, diff):
    """Adjusts percentages to ensure they sum to 100% by adding/subtracting from the last row."""
    if not spending_data.empty:
        spending_data.loc[spending_data.index[-1], 'percentage'] += diff
        spending_data['percentage'] = spending_data['percentage'].round(2)


def update_monthly_spending(task3_response, df):
    """Updates monthly spending trends."""
    monthly_data = df.copy()
    monthly_data['month'] = pd.to_datetime(monthly_data['date']).dt.strftime('%B %Y')

    monthly_income = monthly_data[monthly_data['type'] == 'credit'].groupby('month')['amount'].sum().reset_index()
    monthly_expenses = monthly_data[monthly_data['type'] == 'debit'].groupby('month')['amount'].sum().reset_index()

    monthly_results = pd.merge(monthly_income, monthly_expenses, on='month', how='outer', suffixes=('_income', '_expenses')).fillna(0)
    monthly_results['balance'] = monthly_results['amount_income'] - monthly_results['amount_expenses']

    task3_response['temporal_trends']['monthly_spending'] = monthly_results.rename(columns={'amount_income': 'income', 'amount_expenses': 'expenses'}).to_dict(orient='records')

def process_pdf(uploaded_file):
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    if not text.strip():
        raise ValueError("No text extracted from the PDF.")
    inputs = {'statement_text': text}
    crew_output = Floagentdemo().crew().kickoff(inputs=inputs)
    crew_task_output = complete_json(str(crew_output.tasks_output[-2]))
    # serialized_result = serialize_crew_output(str(crew_output))
    serialized_result = clean_json_output(str(crew_output.tasks_output[-1]))
    analyses_result = update_analysis(serialized_result, crew_task_output)
    return analyses_result, crew_task_output
