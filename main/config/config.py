from dotenv import load_dotenv
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=CURR_DIR+"/env/.env")

SECRET_FLASK_KEY = os.getenv('SECRET_FLASK_KEY')

HOST_URI = os.environ.get("REDIS_HOST_URI")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_CONFIG = {
    "host":HOST_URI,
    "port":REDIS_PORT,
    "username":REDIS_USERNAME,
    "password":REDIS_PASSWORD,
    "user_ttl":3600,
    "api_ttl":30
}

