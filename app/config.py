from pydantic_settings import BaseSettings
from typing import List, Literal

class Settings(BaseSettings):
    api_keys: List[str] = []
    allow_origins: List[str] = ["*"]
    model_backend: Literal["hf","ollama","mock"] = "mock"
    hf_model_id: str = "distilbert-base-uncased"
    ollama_host: str = "http://localhost:11434"

settings = Settings(_env_file=None)
