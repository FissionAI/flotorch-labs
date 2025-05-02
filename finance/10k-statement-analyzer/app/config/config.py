import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if it exists

class Settings:
    #origins
    ORIGINS: str = os.environ.get('ORIGINS')

    #AWS 
    BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
    KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

    #Flotorch
    BASE_URL=os.getenv("BASE_URL")
    API_KEY=os.getenv("API_KEY")

    #Models
    MODELS=os.getenv("MODELS")

    #Fast_API_service
    FASTAPI_SERVICE=os.getenv("FASTAPI_SERVICE","http://localhost:8003")


settings = Settings()