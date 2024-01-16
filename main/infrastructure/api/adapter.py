from typing import Any
from api_interfaces import OpenMeteoApi,WeatherApi
from config.config import OPENMATEO_API_CONFIG,WEATHERAPI_API_CONFIG


class ApiAdapter:
    _initialised = False

    def __init__(self,api,**api_meethods):
        self.api = api

        for key,value in api_meethods.items():
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
    


