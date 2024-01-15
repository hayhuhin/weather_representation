from dotenv import load_dotenv
import os
from pathlib import Path

#* env path 
config_path = Path(__file__).resolve().parent.parent.parent.parent
env_path = config_path/"env"/".env"
load_dotenv(dotenv_path=env_path)

#weatherapi.com env
WEATHERAPI_API_URI = os.environ.get("WEATHERAPI_API_URI")
WEATHERAPI_API_KEY = os.environ.get("WEATHERAPI_API_KEY")
WEATHERAPI_NAME = os.environ.get("WEATHERAPI_NAME")

#openmateo_api env
OPENMETEO_URI = os.environ.get("OPENMETEO_URI")
OPENMETEO_KEY = os.environ.get("OPENMETEO_KEY")
OPENMETEO_SOURCE = os.environ.get("OPENMETEO_SOURCE")


GEO_API_KEY = os.environ.get("GEO_API_KEY")


WEATHERAPI_API_CONFIG= {
    "uri":WEATHERAPI_API_URI,
    "api_key":WEATHERAPI_API_KEY,
    "source":WEATHERAPI_NAME
}


OPENMATEO_API_CONFIG = {
    "uri":OPENMETEO_URI,
    "api_key":OPENMETEO_KEY,
    "source":OPENMETEO_SOURCE,
    "geo_api_key":GEO_API_KEY,
}
IPGEOLOCATION_KEY = os.environ.get("IPGEOLOCATION_API_KEY")



