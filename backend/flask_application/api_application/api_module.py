from dotenv import load_dotenv
import os,json
import requests
from datetime import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry



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
        # self.source = source
        self.test_mode = test_mode


    def queue_micro_service(self):
        """
        this method can have microservices that have to run before each api call.
        for now it only prints that the api called
        """
        #! for now returns always True
        print("api called")
        return True


    def weather_default(self,start_date:str="2024-01-01") -> dict:
        """
        this method queries for a default data of a specific date and returns the data as a json.

        Args:
            start_date(str)="2024-01-01":
                the api call will retrieve data of that specific date .

        Returns:
            api json
        """
        if self.queue_micro_service:
            # end_date = str(date.today())
            get_query = f"{self.uri}/history.json?key={self.key}&q=Israel&dt={start_date}"
            api_request = requests.get(get_query)
            return api_request.json()
    

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


    def weather_by_range(self,request_data:dict) -> dict:
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
            return test_data

        #* this is running before each api call
        if self.queue_micro_service():

            basic_keys = ["start_date","end_date","ip"]
            for keys in basic_keys:
                if keys not in request_data.keys():
                    weather_default = self.weather_default()
                    return weather_default


            start_date = request_data["start_date"]
            end_date = request_data["end_date"]
            user_ip = request_data["ip"]

            get_query = f"{self.uri}/history.json?key={self.key}&q={user_ip}&dt={start_date}&end_dt={end_date}"

            api_request = requests.get(get_query)
            
            return api_request.json()
            


        # http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}



class OpenMeteoApi:
    def __init__(self,uri:str) -> dict:
          
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
        # self.response = self.api_response()



    # def get_user_location_by_ip(self,user_ip):
    #     lan_lat = get_ip_from_api(user_ip)

    #     return 
    # def json_filter_by_day(self,dataframe:pd.DataFrame,specific_date:str) -> dict:
    #     """
    #     this method getting a dataframe data and then filtering it to return specific data by the specific day

    #     Args:
    #         dataframe(pd.dataframe):
    #             large dataframe data that we will need to extract specific date from it 
    #         specific_date(str):
    #             this is the targeted date that we will need to extract from the dataframe

    #     Returns:
    #         json data of the specific date
    #     """
    #     pass



    # def api_response(self) -> pd.DataFrame :
        
    #     responses = self.openmeteo.weather_api(self.uri, params=self.params)
    #     return responses[0]

    def queue_micro_service(self):
        print("api called")
        return True



    def get_daily_json(self,params):
        """
        this method queries the database and returns the daily json that have a large data of each hour from the range od dates

        Returns:
            api dataframe
        """

        if self.queue_micro_service():
            response = self.openmeteo.weather_api(self.uri, params=params)[0]

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
            hourly_data["precipitation_probability"] = hourly_precipitation_probability
            hourly_data["rain"] = hourly_rain
            hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["feelslike_c"] = hourly_apparent_temperature


            hourly_dataframe = pd.DataFrame(data = hourly_data)
            return hourly_dataframe


    def get_week_json(self,params) -> pd.DataFrame:
        """
        this method gets the dayly general data from the specific week

        Returns:
            dataframe of the api responsed json
        """
        if self.queue_micro_service():

            response = self.openmeteo.weather_api(self.uri, params=params)[0]

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

            daily_data["temperature_2m_max"] = daily_temperature_2m_max
            daily_data["temperature_2m_min"] = daily_temperature_2m_min
            daily_data["showers_sum"] = daily_showers_sum
            daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
            daily_data["precipitation_probability_min"] = daily_precipitation_probability_min
            daily_data["precipitation_hours"] = daily_precipitation_hours
            daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max


            daily_dataframe = pd.DataFrame(data = daily_data)
            return daily_dataframe



class ApiController:
    def __init__(self,openmateo_config,weatherapi_config):

        self.openmateo_class = OpenMeteoApi(uri=openmateo_config["uri"])
        self.weatherapi_class = WeatherApi(uri=weatherapi_config["uri"],api_key=weatherapi_config["api_key"],test_mode=weatherapi_config["test_mode"])

    
    def day_data(self,start_date:str) -> dict:
        """
        this method getting the data of the both apis as a dict where the keys are the name of the api and the values is the api json data

        Args:
            start_date(str):
                the specific data of the date
        Returns:
            dict when the keys are the api names and the value is the api response of each api
        """
        
        weather_api_data = self.weatherapi_class.weather_default(start_date=start_date)
        openmateo_data = self.openmateo_class.get_daily_json()
        weather_day_data = {"weatherapi":weather_api_data,"openmateo":openmateo_data}
        
        return weather_day_data 


    def week_data(self,start_date:str,end_date:str,ip:str) -> dict:
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

        weather_api_data = self.weatherapi_class.weather_by_range(request_data={"start_date":start_date,"end_date":end_date,"ip":ip})
        openmateo_api_data = self.openmateo_class.get_week_json()
        weather_week_data = {"weatherapi":weather_api_data,"openmateo":openmateo_api_data}
    
        return weather_week_data 


