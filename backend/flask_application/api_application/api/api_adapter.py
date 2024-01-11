from typing import Any
from .api_module import OpenMeteoApi,WeatherApi
from .config.config import OPENMATEO_API_CONFIG,WEATHERAPI_API_CONFIG



# WEATHERAPI_API_URI = "http://api.weatherapi.com/v1"
# WEATHERAPI_API_KEY = "d3fd130224194172b95202121240101"
# WEATHERAPI_NAME = "weatherapi.com"
# OPENMETEO_URI = "https://api.open-meteo.com/v1/forecast"
# OPENMETEO_KEY = "no key"
# OPENMETEO_SOURCE = "openmateo_api"
# GEO_API_KEY = "eb0ba60b7dbd43738690d24740de2f64"


# WEATHERAPI_API_CONFIG= {
#     "uri":WEATHERAPI_API_URI,
#     "api_key":WEATHERAPI_API_KEY,
#     "source":WEATHERAPI_NAME
# }


# OPENMATEO_API_CONFIG = {
#     "uri":OPENMETEO_URI,
#     "api_key":OPENMETEO_KEY,
#     "source":OPENMETEO_SOURCE,
#     "geo_api_key":GEO_API_KEY,
# }












class ApiAdapter:
    _initialised = False

    def __init__(self,api,**api_meethods):
        self.api = api

        for key,value in api_meethods.items():
            print(value)
            method = getattr(self.api,value)
            self.__setattr__(key,method)
        self._initialised = True
    

    def __getattr__(self, attr) -> Any:
        return getattr(self.api,attr)
    
    
    def __setattr__(self, key:Any, value:Any) -> None:
        
        if not self._initialised:
            super().__setattr__(key,value)
        else:
            setattr(self.api,key,value)



class ApiFacade:
    api_adapters = None



    @classmethod
    def create_day_request(cls):
        print("requesting the day data") 
        cls.api_adapters =[
            ApiAdapter(WeatherApi(uri=WEATHERAPI_API_CONFIG["uri"],api_key=WEATHERAPI_API_CONFIG["api_key"]),request_day_weather="weather_by_day"),
            ApiAdapter(OpenMeteoApi(uri=OPENMATEO_API_CONFIG["uri"],geo_api_key=OPENMATEO_API_CONFIG["geo_api_key"]),request_day_weather="weather_by_day")
        ]
    

    @classmethod
    def create_week_request(cls):
        print("creating the week request")
        cls.api_adapters = [
            ApiAdapter(WeatherApi(uri=WEATHERAPI_API_CONFIG["uri"],api_key=WEATHERAPI_API_CONFIG["api_key"]),request_week_weather="weather_by_week"),
            ApiAdapter(OpenMeteoApi(uri=OPENMATEO_API_CONFIG["uri"],geo_api_key=OPENMATEO_API_CONFIG["geo_api_key"]),request_week_weather="weather_by_week")
        ]


    @classmethod
    def get_day_request(cls,params):
        print("calling the get requests")
        data_dict = {}
        for adapter in cls.api_adapters:
            data = adapter.request_day_weather(params)
            data_dict[adapter.api.name] = data
        return data_dict


    @classmethod
    def get_week_request(cls,params):
        print("calling the week request")
        data_dict = {}
        for adapter in cls.api_adapters:
            data = adapter.request_week_weather(params)
            data_dict[adapter.api.name] = data
        return data_dict
    


