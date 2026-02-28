# expense_agent/config.py

from pathlib import Path

from pydantic_settings import BaseSettings

PACKAGE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    google_genai_use_vertexai: bool = False
    csv_export_dir: Path = PACKAGE_DIR / "exports"

    class Config:
        env_file = ".env"


settings = Settings()
