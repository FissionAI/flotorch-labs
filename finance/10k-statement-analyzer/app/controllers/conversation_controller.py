from fastapi import APIRouter, HTTPException, Response
from app.models.conversation import Conversation
from app.services.conversation_service import create_conversation

router = APIRouter()

@router.post("/")
async def create(response: Response, conversation: Conversation):
    try:
        # Attempt to create the conversation
        result = await create_conversation(conversation)

        # If result is not found, return a 404 error with a message
        if not result:
            return {"error": "Conversation not found", "status": 404}

        # Return the result if successful
        return {"data": result, "status": 200}

    except HTTPException as err:
        # Catch HTTP exceptions and return the error details
        return {"error": err.detail, "status": err.status_code}
    except Exception as e:
        # Catch all other exceptions and return a generic error message
        return {"error": str(e), "status": 500}
