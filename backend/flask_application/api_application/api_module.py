from dotenv import load_dotenv
from pathlib import Path
import os,json
import requests
from datetime import date
from .serializer import WeekDataSerializer
load_dotenv()
CURR_DIR = os.path.dirname(os.path.abspath(__file__))



class ApiCaller:
    """
    this class have methods that sending api requests to the api server by the user

    Methods:
        weather_by_range(user_data(dict)):this getting the requested data like start date end date the the user ip
    """
    
    def __init__(self,uri:str,api_key:str,source:str,test_mode:bool=False):
        self.uri = uri
        self.key = api_key
        self.source = source
        self.test_mode = test_mode


    def queue_micro_service(self):
        """
        later this method will be displayed each time the user will refresh the page and try to requery the api
        this will validate that the user not sending infinite times api calls  
        """
        #! for now returns always True
        print("api called")
        return True


    def weather_default(self,start_date:str="2024-01-01"):
        if self.queue_micro_service:
            # end_date = str(date.today())
            get_query = f"{self.uri}/history.json?key={self.key}&q=Israel&dt={start_date}"
            api_request = requests.get(get_query)
            return api_request.json()
    

    def return_test_data(self):
        with open(CURR_DIR+"/test/mock_data.json","r") as json_file:
            json_data = json.load(json_file)
            return json_data


    #the default method that called first time 
    def weather_by_range(self,request_data:dict):

        #this validates that the user not spamming api requests too many times
################################################################################
        #* this is returning test data if the test mode is on
        if self.test_mode:
            test_data = self.return_test_data()
            return test_data

################################################################################
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
    


