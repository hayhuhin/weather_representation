from dotenv import load_dotenv
from pathlib import Path
import os,json
import requests
from datetime import date
from .serializer import WeekDataSerializer
load_dotenv()
CURR_DIR = os.path.dirname(os.path.abspath(__file__))



mock_data = None
#*this created to work with JsonFilter class
with open(CURR_DIR+"/mock_data.json","r") as json_file:
    json_data = json.load(json_file)
    





class JsonFilter:
    def __init__(self,json_data) -> None:
        self.json = json_data
        print(self.json)
        self.serializer = WeekDataSerializer(location="london",weather_data=self.json["forecast"]["forecastday"])


    def data_by_days(self) -> dict:
        data = self.serializer.daily_data()
        return data


    def specific_day_data(self,date) -> dict:
        days_dict = self.data_by_days()
        hourly_dict = {}
        for items in days_dict[date]["hourly_data"]:
            hourly_dict[items["time"]] = {
                "will_it_rain" :items["will_it_rain"],
                "chance_of_rain" :items["chance_of_rain"],
                "wind_kph" :items["wind_kph"],
                "feelslike_c" :items["feelslike_c"],
                "temp_c" :items["temp_c"],
                # "wind_dir" :items["SE"],
                }

        #first temp_c datastructure
        temp_c_y = []
        temp_c_x = []
        temp_c_y_2 = []


        will_it_rain_x = []
        will_it_rain_y = []
        will_it_rain_y_2 = []


        chance_of_rain_x = []
        chance_of_rain_y = []
        chance_of_rain_y_2 = []


        wind_kph_x = []
        wind_kph_y = []
        wind_kph_y_2 = []


        feelslike_c_x = []
        feelslike_c_y = []
        feelslike_c_y_2 = []

        for hour in hourly_dict:

            #temperature data by hours
            temp_c_x.append(hour)
            temp_c_y.append(hourly_dict[hour]["temp_c"])

            #will it rain
            will_it_rain_x.append(hour)
            will_it_rain_y.append(hourly_dict[hour]["will_it_rain"])


            #chance of rain
            chance_of_rain_x.append(hour)
            chance_of_rain_y.append(hourly_dict[hour]["chance_of_rain"])


            #wind_kph_x
            wind_kph_x.append(hour)
            wind_kph_y.append(hourly_dict[hour]["wind_kph"])


            # feels like 
            feelslike_c_x.append(hour)
            feelslike_c_y.append(hourly_dict[hour]["feelslike_c"])




        #final temperature data that will be served
        temp_c = {
            "y":temp_c_y,
            "x":temp_c_x,
            "y_2":temp_c_y_2

        }

        will_it_rain = {
            "y":will_it_rain_y,
            "x":will_it_rain_x,
            "y_2":will_it_rain_y_2

        }

        chance_of_rain = {
            "y":chance_of_rain_y,
            "x":chance_of_rain_x,
            "y_2":chance_of_rain_y_2

        }

        wind_kph = {
            "y":wind_kph_y,
            "x":wind_kph_x,
            "y_2":wind_kph_y_2

        }
        

        feelslike_c = {
            "y":feelslike_c_y,
            "x":feelslike_c_x,
            "y_2":feelslike_c_y_2

        }


        return temp_c,will_it_rain,chance_of_rain,wind_kph,feelslike_c
    
        

# test = JsonFilter(json_data=json_data)
# data = test.specific_day_data("2023-12-31")
# print(data[0],data[1],data[2],data[3])


class ApiCaller:
    """
    this class have methods that sending api requests to the api server by the user

    Methods:
        weather_by_range(user_data(dict)):this getting the requested data like start date end date the the user ip
    """
    
    def __init__(self,uri,api_key,source):
        self.uri = uri
        self.key = api_key
        self.source = source


    def queue_micro_service(self):
        """
        later this method will be displayed each time the user will refresh the page and try to requery the api
        this will validate that the user not sending infinite times api calls  
        """
        #! for now returns always True
        return True


    def weather_default(self,start_date:str="2024-01-01"):
        # end_date = str(date.today())
        get_query = f"{self.uri}/history.json?key={self.key}&q=Israel&dt={start_date}"
        api_request = requests.get(get_query)
        return api_request.json()
    

    #the default method that called first time 
    def weather_by_range(self,request_data:dict):

        #this validates that the user not spamming api requests too many times
        if self.queue_micro_service():
            basic_keys = ["start_date","end_date","ip"]
            for keys in basic_keys:
                if keys not in request_data.keys():
                    weather_default = self.weather_default()
                    return weather_default


            start_date = request_data["start_date"]
            end_date = request_data["end_date"]
            user_ip = request_data["ip"]

            get_query = f"{self.uri}/history.json?key={self.key}&q={user_ip}&dt={start_date}"


            api_request = requests.get(get_query)
            
            return api_request.json()


        


    #*this was for testing the methods and succesfully created
    # test_api_caller = ApiCaller(uri=BASE_URI+HISTORY,api_key=api_key,source=source)
    # get_weather = test_api_caller.weather_by_range(request_data=data)


    #*this was created for the mock data
    # with open("./backend/api_application/mock_data.json","w") as json_file:
    #     json.dump(get_weather,json_file)
    #     print(get_weather)

    


# #! testing only
# #*this created to work with JsonFilter class
# with open("mock_data.json","r") as json_file:
#     json_data = json.load(json_file)
#     json_filter_class = JsonFilter(json_data=json_data)
#     result = json_filter_class.specific_day_data(date="2024-01-01")
#     # print(result)
    # result = json_filter_class.data_by_days()
    # json_filter_class.hourly_data()
    # print(result["2024-01-01"])
    


