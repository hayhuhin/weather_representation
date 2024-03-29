import os,json
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from .json_serializer import filltered_day_json,filltered_week_json
CURR_DIR = os.path.dirname(os.path.abspath(__file__))






#ip converter to geo location of latitude and longtitude
class IpConverter:
    def __init__(self,api_key,ip_addr):
        self.api_key = api_key
        self.ip = ip_addr


    def queue_micro_service(self):
        print("ip api called")
        
        return True
    

    def geo_location(self):
        if self.queue_micro_service:
            
            query = f'https://api.ipgeolocation.io/timezone?apiKey={self.api_key}&ip={self.ip}'
            
            geo_data = {}
            latitude_api_data = requests.get(query).json()["geo"]["latitude"]
            longitude_api_data = requests.get(query).json()["geo"]["longitude"]

            geo_data["latitude"] = latitude_api_data
            geo_data["longitude"] = longitude_api_data

            return geo_data


#weatherapi API class
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
        self.name = "weatherapi"
        



    def weather_by_day(self,params:dict) -> dict:
        #* this is returning test data if the test_mode is True
        if self.test_mode:
            test_data = self.return_test_data()

            
            filtered_data = filltered_day_json(retrieved_json=test_data,targeted_day=params["start_date"])
            return filtered_data


        #* this is running before each api call
        if self.queue_micro_service():

            basic_keys = ["start_date","end_date","ip"]
            for keys in basic_keys:
                if keys not in params.keys():
                    #this meaning the format of the dict is not correct
                    raise ValueError("the dict is not structured the right way")

            #getting the dict values
            start_date = params["start_date"]
            end_date = params["end_date"]
            user_ip = params["ip"]

            #creating the get api call string
            get_query = f"{self.uri}/forecast.json?key={self.key}&q={user_ip}&dt={start_date}&end_dt={end_date}"

            #requesting the api
            api_request = requests.get(get_query).json()


            #filtering for the dict inot day specific data
            filtered_data = filltered_day_json(retrieved_json=api_request,targeted_day=params["start_date"])

            #calculating the min max data for the insights of the application
            weatherapi_min_max = self.calculate_min_max(filtered_data)

            #adding the source into the dict
            filtered_data["source"] = "weatherapi.com"

            #now creating the final data structured in the wanted manner for the website
            final_data = {**filtered_data,"weatherapi_min_max":weatherapi_min_max,"graph_repr":"day","source":"openmateo.com"}
            
            #returning the data as a dict
            return final_data



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
            filtered_data = filltered_week_json(retrieved_json=test_data)            
            return filtered_data
        

        basic_keys = ["start_date","end_date","ip"]
        for keys in basic_keys:
            if keys not in params.keys():
                #this meaning the format of the dict is not correct
                raise ValueError("the dict is not structured the right way")


        #* this is running before each api call
        if self.queue_micro_service():
        
            #getting the dict values
            start_date = params["start_date"]
            end_date = params["end_date"]
            user_ip = params["ip"]

            #creating the api call string
            get_query = f"{self.uri}/forecast.json?key={self.key}&q={user_ip}&days=7"
            
            #sending the string inot the api call
            api_request = requests.get(get_query).json()

            #now filterring it as the week data json
            filtered_data = filltered_week_json(retrieved_json=api_request)
            
            #returning the filtered data as a dict
            return filtered_data
            

    def calculate_min_max(self,json_data:dict) -> dict:
        """
        this method returns the min and max of each category in the json

        Returns:
            json min max data of each category in the daily json
        """

        #the dict is with th
        
        dict_data = {}
        for items in json_data:
            values = json_data[items]["y"]

            time = json_data[items]["x"]

            min_val = ""
            min_time = ""
            max_val = ""
            max_time = ""
            for index,y in enumerate(values):
                if not max_val:
                    max_val = y

                if not min_val:
                    min_val = y

                if min_val < y:
                    min_val = min_val
                
                else:
                    min_val = y
                    min_time = time[index]

                if max_val > y:
                    max_val = max_val
                
                else:
                    max_val = y
                    max_time = time[index]

            dict_data[items] = {"data":{"min":(min_val,min_time),"max":(max_val,max_time)}},

        return dict_data


    def queue_micro_service(self) -> bool:
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


#openmeteo API class 
class OpenMeteoApi:

    def __init__(self,uri:str,geo_api_key:str,api_key:str="no key",test_mode:bool=False) -> dict:
          
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

        self.geo_api_key = geo_api_key

        self.name = "openmateo"


    def queue_micro_service(self) -> bool:
        """
        most purpose of the function is just to print if the api is called or not
        """
        print("api called")
        return True


    def ip_translator(self,ip:str) ->dict:
        """
        this method is called the ipgeo location api  for getting the lantitude and longtitude 
        of the IP address

        Args:
            ip(str):
                simple IP V4 for example: 8.8.8.8
        
        Returns:
            dict of the geolocation from this ip address
            that structured like this:
            {"latitude":"-15..12312312","longtitude":"114:12121"}
            
        """

        #creating the instance of the ipconverter API class
        ip_converter_class = IpConverter(api_key=self.geo_api_key,ip_addr=ip)

        #using one of its methods to get the dict lantitude and longtitude data
        geo_location = ip_converter_class.geo_location()
        
        #returning dict of tha lng and lon data
        return geo_location


    def weather_by_day(self,params:dict) -> dict:
        """
        this method is calling the API and retrieving the data,then restructuring it as
        needed for the weather application
        the data itself first is represented as dataframe and then transformed into a dict
        Returns:
            filtered json data
        """



        if self.queue_micro_service():

            #simple day data is needed for the api caling
            api_params = {
            "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
            "forecast_days":1,
            }

            #here we are getting the longtitude and lantitude of the IP address
            lan_lat = self.ip_translator(params["ip"])
            
            #here im passing the result of the data above into the dict that will be added 
            #into the api call string
            api_params["longitude"] = lan_lat["longitude"]
            api_params["latitude"] = lan_lat["latitude"]

            #now creating the call to the openmeteo API and getting the first index of the result
            response = self.openmeteo.weather_api(url=self.uri, params=api_params)[0]

            #this whole section is structuring the data as needed for our weather application
            #getting the Hourly data from the openmeteo_requests library
            hourly = response.Hourly()

            #then getting the data that we need specific for our weather app
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

            #structuring the data into the wanted dict 
            hourly_data["chance_of_rain"] = [float(f"{i:.2f}") for i in hourly_precipitation_probability]
            hourly_data["will_it_rain"] = [float(f"{i:.2f}") for i in hourly_rain]
            hourly_data["wind_kph"] = [float(f"{i:.2f}") for i in hourly_wind_speed_10m]
            hourly_data["temp_c"] = [float(f"{i:.2f}") for i in hourly_temperature_2m]
            hourly_data["feelslike_c"] = [float(f"{i:.2f}") for i in hourly_apparent_temperature]

            #because we working with the openmeteo_requests it uses the pandas dataframe library
            df = pd.DataFrame(data = hourly_data)



            #now we creating our last filtered data that we want to serve into our web application
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            openmateo_dict = {
                'temp_c': {'y': df['temp_c'].tolist(), 'x': df['date'].dt.strftime('%H:%M').tolist(), 'y_2': []},
                'will_it_rain': {'y': df['will_it_rain'].tolist(), 'x': df['date'].dt.strftime('%H:%M').tolist(), 'y_2': []},
                'chance_of_rain': {'y': df['chance_of_rain'].tolist(), 'x': df['date'].dt.strftime('%H:%M').tolist(), 'y_2': []},
                'wind_kph': {'y': df['wind_kph'].tolist(), 'x': df['date'].dt.strftime('%H:%M').tolist(), 'y_2': []},
                'feelslike_c': {'y': df['feelslike_c'].tolist(), 'x': df['date'].dt.strftime('%H:%M').tolist(), 'y_2': []}
            }


            #here we getting the min max data that will be represented later in the application
            openmateo_min_max = self.calculate_min_max(openmateo_dict)

            #the final structure of the dict that we want to serve into our weather app
            final_data = {**openmateo_dict,"openmateo_min_max":openmateo_min_max,"graph_repr":"day","source":"openmateo.com"}

            #returning the data as a dict
            return final_data



    def weather_by_week(self,params:dict) -> dict:
        """
        this method gets the dayly general data from the specific week

        Returns:
            weather week json data
        """
        if self.queue_micro_service():


            #this is the basic dict params that will be used inside the API call string
            api_params = {
            "hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
            "forecast_days":7,
            }

            #here we are getting the geo location by an IP
            lan_lat = self.ip_translator(params["ip"])

            #passing the result above into the dict params that will be sent into the API call string
            api_params["longitude"] = lan_lat["longitude"]
            api_params["latitude"] = lan_lat["latitude"]

            #sending the request and retrieving the dataframe response and getting the first index(the data itself) 
            response = self.openmeteo.weather_api(self.uri, params=api_params)[0]

            # getting the Daily data from the openmeteo_requests library 
            daily = response.Daily()

            #getting the specific needed data from the daily data
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_showers_sum = daily.Variables(2).ValuesAsNumpy()
            daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
            daily_precipitation_probability_min = daily.Variables(4).ValuesAsNumpy()
            daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
            daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()

            #simple daily data config data that will be passed for creating a dataframe data
            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s"),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}

            #renaming the data into another name for readability purposes
            daily_data["temp_c"] = daily_temperature_2m_max
            daily_data["will_it_rain"] = daily_showers_sum
            daily_data["chance_of_rain"] = daily_precipitation_probability_max
            daily_data["feelslike_c"] = daily_precipitation_hours
            daily_data["wind_kph"] = daily_wind_speed_10m_max
            
            #creating dataframe object
            df = pd.DataFrame(data = daily_data)

            #! need to recheck the specific data i want to get\
            #* this is not a proper data(avgtemp is feelslike etc...)

            #now filltering and restructuring the data into data that we will be passing into our weather application
            openmateo_dict = {}
            for index, row in df.iterrows():
                date_str = str(row['date'].date())  # Convert date to string
                
                # Extract the relevant information from the DataFrame 
                maxtemp_c = row['temp_c']
                avgtemp_c = row['feelslike_c']
                daily_will_it_rain = row['will_it_rain']
                daily_chance_of_rain = row['chance_of_rain']
                
                # Create a nested dictionary for each date
                date_data = {
                    'maxtemp_c': float(f"{maxtemp_c:.1f}"),
                    'avgtemp_c': float(f"{avgtemp_c:.1f}"),
                    'daily_will_it_rain': float(f"{daily_will_it_rain:.1f}"),
                    'daily_chance_of_rain': float(f"{daily_chance_of_rain:.1f}")
                }
                
                # Add the nested dictionary to the main dictionary with date as the key

                openmateo_dict[date_str] = date_data

                #returning the filltered and structured json data
            return openmateo_dict


    def calculate_min_max(self,json_data:dict) ->dict:
        """
        this method calculates the min max of each field in the json and structuring new dict with the data

        Returns:
            dict with the values of the data
        """



        dict_data = {}

        for items in json_data:
            values = json_data[items]["y"]

            time = json_data[items]["x"]

            min_val = ""
            min_time = ""
            max_val = ""
            max_time = ""
            for index,y in enumerate(values):
                if not max_val:
                    max_val = y

                if not min_val:
                    min_val = y

                if min_val < y:
                    min_val = min_val
                
                else:
                    min_val = y
                    min_time = time[index]

                if max_val > y:
                    max_val = max_val
                
                else:
                    max_val = y
                    max_time = time[index]
            


            dict_data[items] = {"data":{"min":(min_val,min_time),"max":(max_val,max_time)}},
       
        #returning the dict data that will be represented in the weather application
        return dict_data


