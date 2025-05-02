from fastapi import FastAPI
from app.blueprints.conversation import router as conversation_router
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
import json

app = FastAPI()

excluded_paths = ["/api/v1/auth/token", "/api/v1/docs", "/openapi.json", "/docs", "/api/v1/auth/signup"]

# List of allowed origins
origins = json.loads(settings.ORIGINS)

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(conversation_router, prefix="/api/v1")
