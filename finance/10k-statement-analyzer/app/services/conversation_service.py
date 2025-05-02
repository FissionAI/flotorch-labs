from typing import Dict, List, Any
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import HTTPException
from app.models.conversation import Conversation, ModelInfo
from app.config.config import settings
from app.utils.calculate_price import calculate_price_of_model
from app.utils.context_generator import get_context
from flotorch_core.inferencer.gateway_inferencer import GatewayInferencer


def process_model(
    model: ModelInfo,
    user_query: str,
    context: List[Dict[str, str]],
    n_shot_prompt_guide_obj: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handles the inference for a model using the GatewayInferencer.
    """
    try:
        gateway = GatewayInferencer(
            model_id=f"bedrock/{model['value']}",
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
            n_shot_prompts=2,
            n_shot_prompt_guide_obj=n_shot_prompt_guide_obj
        )

        metadata, answer = gateway.generate_text(context=context, user_query=user_query)
        pricing = calculate_price_of_model(model["value"], settings.BEDROCK_REGION, metadata)

        return {
            "answer": answer,
            "metadata": pricing
        }

    except Exception as e:
        return {
            "error": str(e)
        }


async def create_conversation(conversation: Conversation) -> Dict[str, Any]:
    """
    Handles a multi-model conversation request concurrently.
    """
    try:
        # Unpack user query and models
        conversation_dict = conversation.dict(by_alias=True)
        question = conversation_dict["question"]
        models = conversation_dict["models"]

        # Get semantic context using Bedrock KB
        context = get_context(question)

        # Construct system prompt and example guidance
        prompts = {
            "system_prompt": (
                "You are an intelligent assistant that answers questions strictly based on the provided context.\n\n"
                "- Use only the information in the context.\n"
                "- If the answer is not found in the context, respond with: \"I don't know\".\n"
                "- Do not try to make up answers or assumptions.\n"
                "- Keep responses concise and relevant."
            ),
            "examples": [
                {
                    "question": (
                        "Context:\n\"\"\"\nA balance sheet is a financial statement that provides a snapshot of a company's financial position "
                        "at a specific point in time. It includes assets, liabilities, and shareholders' equity. The balance sheet follows the formula: "
                        "Assets = Liabilities + Equity.\n\"\"\"\n\nQuestion: What does a balance sheet include?"
                    ),
                    "answer": "Assets, liabilities, and shareholders' equity"
                },
                {
                    "question": (
                        "Context:\n\"\"\"\nA balance sheet is a financial statement that provides a snapshot of a company's financial position "
                        "at a specific point in time. It includes assets, liabilities, and shareholders' equity. The balance sheet follows the formula: "
                        "Assets = Liabilities + Equity.\n\"\"\"\n\nQuestion: What is the average salary of a financial analyst?"
                    ),
                    "answer": "I don't know"
                }
            ]
        }

        results = {}

        # Run model processing in parallel using a thread pool
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_model = {
                executor.submit(process_model, model, question, context, prompts): model["label"]
                for model in models
            }

            for future in as_completed(future_to_model):
                model_label = future_to_model[future]
                try:
                    results[model_label] = future.result()
                except Exception as e:
                    results[model_label] = {"error": f"Unhandled exception: {str(e)}"}

        return results

    except HTTPException:
        raise  # Allow FastAPI to catch and handle this properly

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
