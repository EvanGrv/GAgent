from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    API_KEY: str = os.getenv("API_KEY", "default_api_key")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID", "default_assistant")
    THREAD_ID: str = os.getenv("THREAD_ID", "default_thread")
    API_KEY_BOX: str = os.getenv("API_KEY_BOX", "default_api_key_box")
    ASSISTANT_ID_BOX: str = os.getenv("ASSISTANT_ID_BOX", "default_assistant_id_box")
    THREAD_ID_BOX: str = os.getenv("THREAD_ID_BOX", "default_thread_id_box")
    MONGO_URI : str = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


SETTINGS = Settings()
