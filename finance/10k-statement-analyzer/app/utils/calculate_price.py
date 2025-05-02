import pandas as pd

def calculate_price_of_model(model_id: str, region: str, metadata: dict) -> dict:
    """
    Calculates the input and output token cost for a specific model based on metadata.
    """

    # Load pricing information from CSV
    df = pd.read_csv("app/docs/bedrock_limits_small.csv")

    # Extract price per token (in USD per million tokens)
    model_input_price = float(
        df[(df['model'] == model_id) & (df['Region'] == region)]['input_price'].values[0]
    )
    model_output_price = float(
        df[(df['model'] == model_id) & (df['Region'] == region)]['output_price'].values[0]
    )

    # Token counts
    input_tokens = float(metadata.get("inputTokens", 0))
    output_tokens = float(metadata.get("outputTokens", 0))

    # Calculate actual cost based on token usage
    input_tokens_cost = round((model_input_price * input_tokens) / 1_000_000, 6)
    output_tokens_cost = round((model_output_price * output_tokens) / 1_000_000, 6)

    # Update metadata with calculated costs
    extended_metadata = {
        **metadata,
        "input_tokens_cost": input_tokens_cost,
        "output_tokens_cost": output_tokens_cost,
        "cost_for_million_such_questions": round(
            1_000_000 * (input_tokens_cost + output_tokens_cost), 4
        )
    }

    return extended_metadata
