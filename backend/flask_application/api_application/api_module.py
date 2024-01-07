from dotenv import load_dotenv
import os,json
import requests
from datetime import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from .json_filter import JsonFilter



        # now = datetime.strptime(start_date, "%Y-%m-%d")
        # timestamp = datetime.timestamp(now)

        # print(timestamp)




load_dotenv()
CURR_DIR = os.path.dirname(os.path.abspath(__file__))



class WeatherApi:
    """
    this class have methods that sending api requests to the api server by the user

    Methods:
        weather_by_range(user_data(dict)):
            this getting the requested data like start date end date the the user ip and queries the api and returns the data as json.
            this method is queries data from specific range for example: start_date:"2024-01-01" end_date:"2024-01-04"

        queue_micro_service:
            this method returns a boolean and its running before each api call.
            later this method will have micro services that have to run before each api call. 

        weather_default(start_date(str)):
            quering the basic api call that called default in my program.
            returns api json of the start_date only.

        
    """
    
    def __init__(self,uri:str,api_key:str,test_mode:bool=False):
        """"
        uri(str):
            must contain the first uri path of the api for example :https://api.myapi.org/data/3.0

        api_key(str):
            the key of the api that will be added later into the query.

        source(str):
            simple the name of the api for example "api.myapi.com"

        test_mode(bool)=False:
            if True it will return mock data and not real query to the api

        ip(str)=None:
            the ip of the user that will query the database
            
        """

        self.uri = uri
        self.key = api_key
        self.test_mode = test_mode
        



    def weather_by_day(self,params:dict) -> dict:



        #* this is returning test data if the test_mode is True
        if self.test_mode:
            test_data = self.return_test_data()

            json_filter = JsonFilter(json_data=test_data)
            filtered_data = json_filter.specific_day_data(date=params["start_date"])            
            return filtered_data


        #* this is running before each api call
        if self.queue_micro_service():

            basic_keys = ["start_date","end_date","ip"]
            for keys in basic_keys:
                if keys not in params.keys():
                    weather_default = self.weather_default()
                    return weather_default


            start_date = params["start_date"]
            end_date = params["end_date"]
            user_ip = params["ip"]

            get_query = f"{self.uri}/history.json?key={self.key}&q={user_ip}&dt={start_date}&end_dt={end_date}"

            api_request = requests.get(get_query).json()
            json_filter = JsonFilter(json_data=api_request)

            filtered_data = json_filter.specific_day_data(date=params["start_date"])
            
            return filtered_data



    def weather_by_week(self,params:dict) -> dict:
        """
        this method is getting data from the api by the range of dates.
        if test_mode is True it will not query and return a mock json

        Args:
            request_data(dict):
                the dict structure have to be like this:
                    {
                    "start_date":"2024-01-01",
                    "end_date":"2024-01-05",
                    "ip":"80.192.64.50"
                    }
        
                    
        Returns :
            api json data
        """



        #* this is returning test data if the test_mode is True
        if self.test_mode:
            test_data = self.return_test_data()
            json_filter = JsonFilter(json_data=test_data)
            filtered_data = json_filter.specific_week_data(start_date=params["start_date"],end_date=params["end_date"])            
            return filtered_data


        #* this is running before each api call
        if self.queue_micro_service():

            start_date = params["start_date"]
            end_date = params["end_date"]
            user_ip = params["ip"]

            get_query = f"{self.uri}/history.json?key={self.key}&q={user_ip}&dt={start_date}&end_dt={end_date}"
            api_request = requests.get(get_query).json()
            json_filter = JsonFilter(json_data=api_request)
            filtered_data = json_filter.specific_week_data(start_date=params["start_date"],end_date=params["end_date"])
            return filtered_data
            


    def queue_micro_service(self):
        """
        this method can have microservices that have to run before each api call.
        for now it only prints that the api called
        """
        #! for now returns always True
        print("api called")
        return True



    def return_test_data(self) -> dict:
        """
        this method loading json moch data and returning it
        most of the usage is for testing only

        Returns:
            json data
        """
        with open(CURR_DIR+"/test/mock_data.json","r") as json_file:
            json_data = json.load(json_file)
            return json_data



class OpenMeteoApi:
    def __init__(self,uri:str,api_key:str="no key",test_mode:bool=False) -> dict:
          
        """
        constructor method of the openmeteoapi class

        Args:
        uri(str):
            the uri of the api call as string.
        
        params(dict):
            for more details about the params structure: https://open-meteo.com/en/docs
            this dict structure have to be like that:
                {
                    "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
                    "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
                    "forecast_days":1,
                        "past_days":7,
                }
        user_lat_lan(dict):
            its the user latitude and langtitude for the api position
            this two args have to be inside the params but this data cant be added before this class is initialised so we must first 
            get the user ip address and only then pass it into the api params
        """   
        
        
        self.uri = uri
        # self.params = params
        self.cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = self.retry_session)
        self.test_mode = test_mode




    def queue_micro_service(self):
        print("api called")
        return True


    def ip_translator(self,ip):
        data = {"latitude": 32.028320,
	            "longitude": 34.781879,}

        return data



    def weather_by_day(self,params):
        """
        this method queries the database and returns the daily json that have a large data of each hour from the range od dates

        Returns:
            api dataframe
        """



        if self.queue_micro_service():


            api_params = {
            "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
            "forecast_days":1,
            }

            lan_lat = self.ip_translator(params["ip"])
            api_params["longitude"] = lan_lat["longitude"]
            api_params["latitude"] = lan_lat["latitude"]
            response = self.openmeteo.weather_api(url=self.uri, params=api_params)[0]

            hourly = response.Hourly()
            hourly_precipitation_probability = hourly.Variables(0).ValuesAsNumpy()
            hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
            hourly_rain = hourly.Variables(2).ValuesAsNumpy()
            hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
            hourly_temperature_2m = hourly.Variables(4).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s"),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
            )}
            hourly_data["chance_of_rain"] = hourly_precipitation_probability
            hourly_data["will_it_rain"] = hourly_rain
            hourly_data["wind_kph"] = hourly_wind_speed_10m
            hourly_data["temp_c"] = hourly_temperature_2m
            hourly_data["feelslike_c"] = hourly_apparent_temperature

# df['date'] = pd.to_datetime(df['date'], unit='ms')

# Create a new DataFrame with the desired structure




            df = pd.DataFrame(data = hourly_data)

            result_df = pd.DataFrame({
                
                    'temp_c': {'y': df['temp_c'].tolist(), 'x': df['date'].dt.strftime('%Y-%m-%d %H:%M').tolist(), 'y_2': []},
                    'will_it_rain': {'y': df['will_it_rain'].tolist(), 'x': df['date'].dt.strftime('%Y-%m-%d %H:%M').tolist(), 'y_2': []},
                    'chance_of_rain': {'y': df['chance_of_rain'].tolist(), 'x': df['date'].dt.strftime('%Y-%m-%d %H:%M').tolist(), 'y_2': []},
                    'wind_kph': {'y': df['wind_kph'].tolist(), 'x': df['date'].dt.strftime('%Y-%m-%d %H:%M').tolist(), 'y_2': []},
                    'feelslike_c': {'y': df['feelslike_c'].tolist(), 'x': df['date'].dt.strftime('%Y-%m-%d %H:%M').tolist(), 'y_2': []}
                ,
            })

            # print(hourly_dataframe.to_json())for i in 
            json_result = result_df.to_json()

            return json_result




    def weather_by_week(self,params) -> pd.DataFrame:
        """
        this method gets the dayly general data from the specific week

        Returns:
            dataframe of the api responsed json
        """
        if self.queue_micro_service():


            api_params = {
            "past_days":7,
            "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
            "forecast_days":1,
            }
            lan_lat = self.ip_translator(params["ip"])
            api_params["longitude"] = lan_lat["longitude"]
            api_params["latitude"] = lan_lat["latitude"]

            response = self.openmeteo.weather_api(self.uri, params=api_params)[0]

            # Process daily data. The order of variables needs to be the same as requested.
            daily = response.Daily()
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_showers_sum = daily.Variables(2).ValuesAsNumpy()
            daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
            daily_precipitation_probability_min = daily.Variables(4).ValuesAsNumpy()
            daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
            daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()


            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s"),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}

            daily_data["temp_c"] = daily_temperature_2m_max
            # daily_data["temperature_2m_min"] = daily_temperature_2m_min
            daily_data["will_it_rain"] = daily_showers_sum
            daily_data["chance_of_rain"] = daily_precipitation_probability_max
            # daily_data["precipitation_probability_min"] = daily_precipitation_probability_min
            daily_data["feelslike_c"] = daily_precipitation_hours
            daily_data["wind_kph"] = daily_wind_speed_10m_max
            daily_dataframe = pd.DataFrame(data = daily_data)


            return daily_dataframe




class ApiController:
    def __init__(self,openmateo_config,weatherapi_config,test_mode:bool):

        self.openmateo_class = OpenMeteoApi(uri=openmateo_config["uri"])
        self.weatherapi_class = WeatherApi(uri=weatherapi_config["uri"],api_key=weatherapi_config["key"],test_mode=test_mode)

    
    def day_data(self,params:dict) -> dict:
        """
        this method getting the data of the both apis as a dict where the keys are the name of the api and the values is the api json data

        Args:
            start_date(str):
                the specific data of the date
        Returns:
            dict when the keys are the api names and the value is the api response of each api
        """

        #TODO getting the latitude and langtitude of an ip address
        
        weather_api_data = self.weatherapi_class.weather_by_day(params=params)
        openmateo_data = self.openmateo_class.weather_by_day(params=params)

        weather_day_data = {"weatherapi":weather_api_data,"openmateo":openmateo_data}
        
        return weather_day_data


    def week_data(self,params:dict) -> dict:
        """
        this method getting the data of the both apis as a dict where the keys are the name of the api and the values is the api json data

        Args:
            start_date(str):
                the start date of the api request
            end_date(str):
                the end date of the api request
            ip(str):
                the ip of the user that will be used to search in the api by location

        Returns:
            dict of the json data
        """

        weather_api_data = self.weatherapi_class.weather_by_week(params=params)
        openmateo_api_data = self.openmateo_class.weather_by_week(params=params)
        weather_week_data = {"weatherapi":weather_api_data,"openmateo":openmateo_api_data}
    
        return weather_week_data 




#*checking the weatherapi methods and all is good
# WEATHERAPI_API_URI = "http://api.weatherapi.com/v1"
# WEATHERAPI_API_KEY = "d3fd130224194172b95202121240101"
# WEATHERAPI_NAME = "weatherapi.com"
# test = WeatherApi(uri=WEATHERAPI_API_URI,api_key="",test_mode=True)


# requested_data = {
#     "start_date":"2024-01-01",
#     "end_date":"2023-12-27",
#     "ip":"8.8.8.8",
# }



# data = test.weather_by_day(request_data=requested_data)


#*checking the openmeteo api 
OPENMETEO_URI = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_KEY = "no key"
OPENMETEO_SOURCE = "openmateo_api"




# day_params = {
# 	"hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
# 	"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
# 	"forecast_days":1,
# }

# week_params = {
#     "past_days":7,
#     "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
# 	"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
# 	"forecast_days":1,
# }





#! will be used later in the production website
OPENMETEO_URI = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_KEY = "no key"
OPENMETEO_SOURCE = "openmateo_api"

WEATHERAPI_API_URI = "http://api.weatherapi.com/v1"
WEATHERAPI_API_KEY = "d3fd130224194172b95202121240101"
WEATHERAPI_NAME = "weatherapi.com"


OPENMATEO_API_CONFIG = {
    "uri":OPENMETEO_URI,
    "api_key":OPENMETEO_KEY,
    "source":OPENMETEO_SOURCE,
}

WEATHERAPI_API_CONFIG = {
        "uri":WEATHERAPI_API_URI,
        "api_key":WEATHERAPI_API_KEY,
        "source":WEATHERAPI_NAME,
        "test_mode":True
}



# test_class = ApiController(openmateo_config=OPENMATEO_API_CONFIG,weatherapi_config=WEATHERAPI_API_CONFIG)
# basic_data = {
#     "start_date":"2024-01-01",
#     "end_date":"2023-12-26",
#     "ip":"8.8.8.8"
# }
# day_data = test_class.day_data(params=basic_data)
# week_data = test_class.week_data(params=basic_data)

#! will be used later in the production website
