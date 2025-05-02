import traceback
from flotorch_core.storage.db.vector.vector_storage_factory import VectorStorageFactory
from flotorch_core.chunking.chunking import Chunk
from app.config.config import settings


def get_context(question: str, top_k: int = 5) -> list:
    """
    Generate vector-based context from a Bedrock-powered knowledge base.

    Args:
        question (str): The user's natural language query.
        top_k (int): Number of top relevant documents to retrieve.

    Returns:
        list: A list of retrieved context documents (as JSON objects).
    """
    def _initialize_vector_storage(bedrock_kb_id: str, aws_region: str):
        """
        Internal helper to create and return a Bedrock vector storage instance.

        Args:
            bedrock_kb_id (str): ID of the Bedrock knowledge base.
            aws_region (str): AWS region of the knowledge base.

        Returns:
            An instance of vector storage configured with Bedrock.
        """
        return VectorStorageFactory.create_vector_storage(
            knowledge_base=True,
            use_bedrock_kb=True,
            embedding=None,  # No manual embedding needed when using Bedrock KB
            knowledge_base_id=bedrock_kb_id,
            aws_region=aws_region
        )

    try:
        # Initialize storage
        vector_storage = _initialize_vector_storage(settings.KNOWLEDGE_BASE_ID, settings.BEDROCK_REGION)

        # Convert question to chunk and search top_k results
        question_chunk = Chunk(data=question)
        search_result = vector_storage.search(question_chunk, top_k)

        # Return only the list of matched results
        return search_result.to_json().get('result', [])

    except Exception as e:
        # Handle any unexpected exceptions
        traceback_str = traceback.format_exc()  # Get full traceback details
        print(f"Error occurred in get_context: {str(e)}")
        print(f"Traceback: {traceback_str}")
        raise Exception(f"Error while processing context: {str(e)}") from e
