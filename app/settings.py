from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

HOST: str = config("HOST", cast=str, default="0.0.0.0")
PORT: int = config("PORT", cast=int, default=8080)

DEBUG: bool = config("DEBUG", cast=bool, default=False)
RELOAD: bool = config("RELOAD", cast=bool, default=False)
LOG_LEVEL: str = config("LOG_LEVEL", cast=str, default="info")

ALLOW_ORIGINS = config("ALLOW_ORIGINS", cast=CommaSeparatedStrings, default="*")
ALLOW_HEADERS = config("ALLOW_HEADERS", cast=CommaSeparatedStrings, default="*")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*")

DATA_BASE_PATH = config("DATA_BASE_PATH", default="data")

MODEL_NAME = config("MODEL_NAME", cast=str, default="llama-3.3-70b-versatile")

GROQ_API_KEY = config("GROQ_API_KEY", cast=str, default="")

DB_NAME = config("DB_NAME", cast=str, default="vector_db")
COLLECTION_NAME = config("COLLECTION_NAME", cast=str, default="bank-website")
N_RESULTS = config("N_RESULTS", cast=int, default=15)
THRESHOLD = config("THRESHOLD", cast=float, default=0.75)
