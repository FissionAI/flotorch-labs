import streamlit as st
import requests
import json
from typing import Dict, List
from app.config.config import settings


def get_model_responses(query: str, models_data: List[Dict]) -> Dict:
    """
    Send the query and selected models to the FastAPI backend and return model responses.

    Args:
        query (str): User input query.
        models_data (List[Dict]): List of selected model dicts with label, value, and service.

    Returns:
        Dict: JSON response from the backend.
    """
    try:
        response = requests.post(
            f"{settings.FASTAPI_SERVICE}/api/v1/session/conversation",
            json={
                "question": query,
                "models": models_data
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return {}


def main():
    st.set_page_config(layout="wide")
    st.title("10K Statement Analyzer")

    # Load model info from config and convert to lookup dict
    models = json.loads(settings.MODELS)
    llm_models = {model['label']: model for model in models}
    all_labels = list(llm_models.keys())

    st.info("Analyze 10-K filings (2022–2024) for Apple, Amazon, Google, Microsoft, Netflix, Intel, NVIDIA, and Tesla")

    sample_questions = [
        "What was the year-over-year growth in NVIDIA's Data Center revenue in fiscal year 2024, as stated in their 10-K?",
        "How did Microsoft's spending on sales and marketing change in fiscal year 2024, and what were the main reasons for this change?",
        "What were Apple's net sales for the fiscal year ending in 2024, broken down by product category (e.g., iPhone, Mac, iPad, Wearables, Services)?",
        "What were Netflix’s net profits in each year from 2022 to 2024?",
        "What were the Microsoft's total revenues for the fiscal year?"
    ]

    # Store selected question from session state
    st.session_state.setdefault("selected_question", "")

    st.subheader("📋 Sample Questions")

    for idx, q in enumerate(sample_questions):
        cols = st.columns([6, 1])
        cols[0].markdown(f"**{q}**")
        if cols[1].button("Use", key=f"use_btn_{idx}"):
            st.session_state.selected_question = q

    # User input area
    user_input = st.text_area("Enter your query:", st.session_state.selected_question, height=100)

    # Model selection dropdowns
    col1, col2, col3 = st.columns(3)
    with col1:
        model1 = st.selectbox("Select Model 1", ["None"] + all_labels)
    with col2:
        model2 = st.selectbox("Select Model 2", ["None"] + [m for m in all_labels if m != model1])
    with col3:
        model3 = st.selectbox("Select Model 3", ["None"] + [m for m in all_labels if m not in {model1, model2}])

    selected_models = list(filter(lambda m: m != "None", [model1, model2, model3]))

    # Submit button
    if st.button("Generate Responses"):
        if not user_input:
            st.warning("Please enter a query.")
            return

        if not selected_models:
            st.warning("Please select at least one model.")
            return

        # Prepare model data for backend
        selected_model_data = [
            {
                "label": model,
                "value": llm_models[model]['value'],
                "service": llm_models[model]['service']
            }
            for model in selected_models
        ]

        with st.spinner("Generating responses..."):
            responses = get_model_responses(user_input, selected_model_data)

            # Display responses in columns
            for idx, model in enumerate([model1, model2, model3]):
                if model and model != "None":
                    with [col1, col2, col3][idx]:
                        st.subheader(model)
                        response = responses.get('data', {}).get(model)

                        if isinstance(response, dict):
                            if "error" in response:
                                st.error(f"Error from {model}: {response['error']}")
                            else:
                                st.markdown(response.get("answer", "No answer found.").replace("$", "\\$"))
                                st.json(response.get("metadata", {}))
                        elif isinstance(response, str):
                            st.markdown(response)
                        else:
                            st.warning("Unexpected response format.")


if __name__ == "__main__":
    main()
