from dotenv import load_dotenv
import os
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent/"env"/".env"
#loading env variables
load_dotenv(dotenv_path=env_path)

SECRET_FLASK_KEY = os.getenv('SECRET_FLASK_KEY')

#redis configuration structure
HOST_URI = os.environ.get("REDIS_HOST_URI")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

#redis configuration structure
REDIS_CONFIG = {
    "host":HOST_URI,
    "port":REDIS_PORT,
    "username":REDIS_USERNAME,
    "password":REDIS_PASSWORD,
    "user_ttl":3600,
    "api_ttl":30
}

