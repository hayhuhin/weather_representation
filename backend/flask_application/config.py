from dotenv import load_dotenv
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=CURR_DIR+"/env/.env")

SECRET_FLASK_KEY = os.getenv('SECRET_FLASK_KEY')

HOST_URI = os.environ.get("REDIS_HOST_URI")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

#weatherapi.com env
WEATHERAPI_API_URI = os.environ.get("WEATHERAPI_API_URI")
WEATHERAPI_API_KEY = os.environ.get("WEATHERAPI_API_KEY")
WEATHERAPI_NAME = os.environ.get("WEATHERAPI_NAME")

#openmateo_api env
OPENMETEO_URI = os.environ.get("OPENMETEO_URI")
OPENMETEO_KEY = os.environ.get("OPENMETEO_KEY")
OPENMETEO_SOURCE = os.environ.get("OPENMETEO_SOURCE")


REDIS_CONFIG = {
    "host":HOST_URI,
    "port":REDIS_PORT,
    "username":REDIS_USERNAME,
    "password":REDIS_PASSWORD
}


WEATHERAPI_API_CONFIG= {
    "uri":WEATHERAPI_API_URI,
    "key":WEATHERAPI_API_KEY,
    "source":WEATHERAPI_NAME
}


OPENMATEO_API_CONFIG = {
    "uri":OPENMETEO_URI,
    "key":OPENMETEO_KEY,
    "source":OPENMETEO_SOURCE,
}


OPENMATEO_API_PARAMS = {
    "past_days":7,
	"hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
	"forecast_days":1,
}

