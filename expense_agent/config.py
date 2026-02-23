# expense_agent/expense_agent/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    google_genai_use_vertexai: bool = False

    class Config:
        env_file = ".env"

settings = Settings()