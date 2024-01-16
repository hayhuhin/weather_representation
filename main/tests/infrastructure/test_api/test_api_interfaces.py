from pathlib import Path
import pytest
import sys
#importing the api interfaces
sys.path.append("../../../infrastructure/api")
from api_interfaces import WeatherApi,OpenMeteoApi
from config.config import WEATHERAPI_API_CONFIG,OPENMATEO_API_CONFIG,IPGEOLOCATION_KEY

