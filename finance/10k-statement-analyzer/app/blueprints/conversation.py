from fastapi import APIRouter
from app.controllers.conversation_controller import router as conversation_router

router = APIRouter()
router.include_router(conversation_router, prefix="/session/conversation", tags=["conversation"])