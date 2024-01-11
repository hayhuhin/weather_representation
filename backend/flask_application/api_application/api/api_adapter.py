from typing import Any
from api_module import OpenMeteoApi,WeatherApi
from config.config import OPENMATEO_API_CONFIG,WEATHERAPI_API_CONFIG,IPGEOLOCATION_KEY



#! testing only
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

# required_data = {
#     "start_date":"2024-01-10",
#     "end_date":"2024-01-11",
#     "ip":"8.8.8.8"
# }
#! testing only



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
    
    
    def __setattr__(self, key, value: Any) -> None:
        
        if not self._initialised:
            super().__setattr__(key,value)
        else:
            setattr(self.api,key,value)



class ApiFacade:
    api_adapters = None



    @classmethod
    def create_day_request(cls,params):
        print("requesting the day data") 
        cls.api_adapters =[
            ApiAdapter(WeatherApi(uri=WEATHERAPI_API_CONFIG["uri"],api_key=WEATHERAPI_API_CONFIG["api_key"]),request_day_weather="weather_by_day",params=params),
            ApiAdapter(OpenMeteoApi(uri=OPENMATEO_API_CONFIG["URI"],geo_api_key=IPGEOLOCATION_KEY),request_day_weather="weather_by_day",params=params)
        ]
    
    @classmethod
    def create_week_request(cls,params):
        print("creating the week request")
        cls.api_adapters = [
            ApiAdapter(WeatherApi(uri=WEATHERAPI_API_CONFIG["uri"],api_key=WEATHERAPI_API_CONFIG["api_key"]),request_week_weather="weather_by_week",params=cls.required_data),
            ApiAdapter(OpenMeteoApi(uri=OPENMATEO_API_CONFIG["URI"],geo_api_key=IPGEOLOCATION_KEY),request_week_weather="weather_by_week",params=cls.required_data)
        ]

    @classmethod
    def get_day_request(cls):
        print("calling the get requests")
        for adapter in cls.api_adapters:
            data = adapter.request_day_weather()
            return data


    @classmethod
    def get_week_request(cls):
        print("calling the week request")
        for adapter in cls.api_adapters:
            data = adapter.request_week_weather()
            return data



# class ApiController:
#     def __init__(self,openmateo_config,weatherapi_config,test_mode:bool):

#         self.openmateo_class = OpenMeteoApi(uri=openmateo_config["uri"],geo_api_key=openmateo_config["geo_api_key"])
#         self.weatherapi_class = WeatherApi(uri=weatherapi_config["uri"],api_key=weatherapi_config["api_key"],test_mode=test_mode)

  
#     def day_data(self,params:dict) -> dict:
#         """
#         this method getting the data of the both apis as a dict where the keys are the name of the api and the values is the api json data

#         Args:
#             start_date(str):
#                 the specific data of the date
#         Returns:
#             dict when the keys are the api names and the value is the api response of each api
#         """

#         #TODO getting the latitude and langtitude of an ip address
        
#         weather_api_data = self.weatherapi_class.weather_by_day(params=params)
#         openmateo_data = self.openmateo_class.weather_by_day(params=params)

#         weather_min_max = self.weatherapi_class.calculate_min_max(weather_api_data)
#         openmateo_min_max = self.openmateo_class.calculate_min_max(openmateo_data)

#         weather_api_data["source"] = "weatherapi.com"
#         openmateo_data["source"] = "openmateoapi.com"
#         weather_day_data = {"weatherapi":weather_api_data,"openmateo":openmateo_data,"weatherapi_min_max":weather_min_max,"openmateo_min_max":openmateo_min_max}

#         return weather_day_data


#     def week_data(self,params:dict) -> dict:
#         """
#         this method getting the data of the both apis as a dict where the keys are the name of the api and the values is the api json data

#         Args:
#             start_date(str):
#                 the start date of the api request
#             end_date(str):
#                 the end date of the api request
#             ip(str):
#                 the ip of the user that will be used to search in the api by location

#         Returns:
#             dict of the json data
#         """

#         weather_api_data = self.weatherapi_class.weather_by_week(params=params)
#         openmateo_api_data = self.openmateo_class.weather_by_week(params=params)
#         weather_week_data = {"weatherapi":weather_api_data,"openmateo":openmateo_api_data}
    
#         return weather_week_data 





# if __name__ == "__main__":
#     ApiFacade.create_week_request()
#     ApiFacade.get_week_request()
