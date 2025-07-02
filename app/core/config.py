import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI:str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "")
    MONGODB_COLLECTION_NAME: str = os.getenv("MONGODB_COLLECTION_NAME", "")
    MONGO_ATLAS_SEARCH_INDEX: str = os.getenv("MONGO_ATLAS_SEARCH_INDEX", "vector_index")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY","")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")

Variable = Settings()