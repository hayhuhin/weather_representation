from dotenv import load_dotenv
from pathlib import Path
import os
import requests
from settings import BASE_URI,HISTORY,Q,DATE_TIME,END_DATE,KEY
load_dotenv()



class ApiCaller(object):
    
    def __init__(self,uri,api_key):
        self.uri = uri
        self.key = api_key

    
    #the default method that called first time 
    def weather_default(self,user,user_position):
        start_date = "2024-01-01"
        end_date = "2024-01-01"
        get_query = self.uri+KEY+self.key+Q+user_position+DATE_TIME+start_date
        # print(get_query)
        api_request = requests.get(get_query)
        print(api_request.json())



if __name__ == "__main__":
    test = ApiCaller(uri=BASE_URI+HISTORY,api_key=os.getenv("API_KEY"))

    get_weather = test.weather_default(user="valeri",user_position="2a00:a040:1a3:dfe9:f137:4f80:d019:8b79")


