
from api_application.redis_module import RedisConnector
# from api_application.api_module import ApiCaller
# from backend.flask_application.api_application.api.json_filter import JsonFilter
from api_application.graph_module import GraphRepresantation
# from backend.flask_application.api_application.api.api_module import ApiController
from api_application.api.api_adapter import ApiFacade


# from config import CURR_DIR,SECRET_FLASK_KEY,HOST_URI,REDIS_PORT,REDIS_USERNAME,REDIS_PASSWORD,WEATHERAPI_API_KEY,WEATHERAPI_API_URI

# # redis_client = RedisConnector(host=HOST_URI,port=REDIS_PORT,username=REDIS_USERNAME,password=REDIS_PASSWORD)
# api_connector = ApiCaller(uri=WEATHERAPI_API_URI,api_key=WEATHERAPI_API_KEY,source="weather_api")
# graph_repr = GraphRepresantation()

# self.api_1 = ApiCaller(uri=api_1_config["uri"],api_key=api_1_config["key"],source=api_1_config["source"],test_mode=test_mode)
# self.api = ApiController(openmateo_config=OPENMATEO_API_CONFIG,weatherapi_config=WEATHERAPI_API_CONFIG)
# self.api_2 = ApiCaller(uri=api_2_config["uri"],api_key=api_2_config["key"],source=api_2_config["source"])




class ControllerClass:
    def __init__(self,redis_config:dict,test_mode:bool=False):
        self.redis = RedisConnector(host=redis_config["host"],port=redis_config["port"],username=redis_config["username"],password=redis_config["password"])
        self.api_facade = ApiFacade()
        self.graph_repr = GraphRepresantation()
        self.user_ttl = redis_config["user_ttl"]
        self.api_ttl = redis_config["api_ttl"]


    def first_time(self,start_date,end_date,ip):
        params = {
            "start_date":start_date,
            "end_date":end_date,
            "ip":ip,
        }


        #*creating the request from the api's and then getting the data
        self.api_facade.create_day_request(params=params)
        day_data = self.api_facade.get_day_request()

        #this adding the cache data into the redis db
        result = self.redis.set_key(key=ip,value={"user_data":day_data,"graph_repr":"day"})

    

    def change_state(self,state:str,start_date:str,end_date:str,ip:str):
        #first we checking if the user already sent api request in the last 30 sec

        timer_is_set = self.redis.check_timer(key=ip)
        if timer_is_set:
            print(f"you have ttl and have to wait atleast {timer_is_set}")
            return {"error":"you have ttl for the query"}


        if state == "week":

            params = {
            "start_date":start_date,
            "end_date":end_date,
            "ip":ip,
            }
            
            api_data = self.api.week_data(params=params)

            #first we delete the existing data if any
            self.redis.clear_all(ip)

            #this adding the cache data into the redis db
            self.redis.set_key(key=ip,value={"user_data":api_data,"graph_repr":"week"},timer=self.api_ttl)
            
        
        if state == "day":

            params = {
            "start_date":start_date,
            "end_date":start_date,
            "ip":ip,
            }
            api_data = self.api.day_data(params=params)
            
            #first we delete the existing data if any
            self.redis.clear_all(ip)

            #this adding the cache data into the redis db
            result = self.redis.set_key(key=ip,value={"user_data":api_data,"graph_repr":"day"},timer=self.api_ttl)

        

    #TODO add the option to change the graph repr from line to bar graph
    def day_view(self,required_data,graph_type:str="line_graph_compared") -> str:



        # print(required_data["user_data"]["openmateo"])

        source1 = required_data["user_data"]["weatherapi"]["source"]
        source2 = required_data["user_data"]["openmateo"]["source"]

        temp_c = required_data["user_data"]["weatherapi"]["temp_c"]
        temp_c["y_2"] = required_data["user_data"]["openmateo"]["temp_c"]["y"]
        temp_c["DB_1"] = source1
        temp_c["DB_2"] = source2

        will_it_rain = required_data["user_data"]["weatherapi"]["will_it_rain"]
        will_it_rain["y_2"] = required_data["user_data"]["openmateo"]["will_it_rain"]["y"]

        will_it_rain["DB_1"] = source1
        will_it_rain["DB_2"] = source2

        chance_of_rain = required_data["user_data"]["weatherapi"]["chance_of_rain"]
        chance_of_rain["y_2"] = required_data["user_data"]["openmateo"]["chance_of_rain"]["y"]

        chance_of_rain["DB_1"] = source1
        chance_of_rain["DB_2"] = source2

        wind_kph = required_data["user_data"]["weatherapi"]["wind_kph"]
        wind_kph["y_2"] = required_data["user_data"]["openmateo"]["wind_kph"]["y"]

        wind_kph["DB_1"] = source1
        wind_kph["DB_2"] = source2

        feelslike_c = required_data["user_data"]["weatherapi"]["feelslike_c"]
        feelslike_c["y_2"] = required_data["user_data"]["openmateo"]["feelslike_c"]["y"]

        feelslike_c["DB_1"] = source1
        feelslike_c["DB_2"] = source2


        # print(graph_type)
        # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
        temp_c_html = self.graph_repr.graph_options(graph_type=graph_type,dict_values=temp_c,graph_repr="1_row",path="")
        will_it_rain_html= self.graph_repr.graph_options(graph_type=graph_type,dict_values=will_it_rain,graph_repr="1_row",path="")
        chance_of_rain_html = self.graph_repr.graph_options(graph_type=graph_type,dict_values=chance_of_rain,graph_repr="1_row",path="")
        wind_kph_html = self.graph_repr.graph_options(graph_type=graph_type,dict_values=wind_kph,graph_repr="1_row",path="")
        feelslike_c_html = self.graph_repr.graph_options(graph_type=graph_type,dict_values=feelslike_c,graph_repr="1_row",path="")



        openmateo_min_max = required_data["user_data"]["openmateo_min_max"]
        weatherapi_min_max = required_data["user_data"]["weatherapi_min_max"]



        weather_day_graph = {
            "temp_c":{
                "html":temp_c_html,
                "data":{
                    "name":"temperature",
                    "appearance":source1,
                    "information":{
                        "weatherapi":weatherapi_min_max["temp_c"],
                        "openmateo":openmateo_min_max["temp_c"],
                                  }
                        }
                    },
            "will_it_rain":{
                "html":will_it_rain_html,
                "data":{
                    "name":"will it rain",
                    "appearance":source1,
                    "information":{
                        "weatherapi":weatherapi_min_max["will_it_rain"],
                        "openmateo":openmateo_min_max["will_it_rain"],
                                    }
                        }
                    },
            "chance_of_rain":{
                "html":chance_of_rain_html,
                "data":{
                    "name":"chance of rain",
                    "appearance":source1,
                    "information":{
                        "weatherapi":weatherapi_min_max["chance_of_rain"],
                        "openmateo":openmateo_min_max["chance_of_rain"],
                                }
                        }
                    },
            "wind_kph":{
                "html":wind_kph_html,
                "data":{
                    "name":"wind kph",
                    "appearance":source1,
                    "information":{
                        "weatherapi":weatherapi_min_max["wind_kph"],
                        "openmateo":openmateo_min_max["wind_kph"],
                                }
                        }
                    },
            "feelslike_c":{
                "html":feelslike_c_html,
                "data":{
                    "name":"feels like ",
                    "appearance":source1,
                    "information":{
                        "weatherapi":weatherapi_min_max["feelslike_c"],
                        "openmateo":openmateo_min_max["feelslike_c"],
                                    }
                        }
                    },
            }

        return weather_day_graph


    def week_view(self,required_data):

        #must be fixed because there is no realy graph is needed and only cards
        #to display the different weathers
        # redis_dict = self.redis.get(key=self.ip)
        #*this dict is store as a nested dict 
        #*main key is {date:{"maxtemp":"10","mintemp":-10}}
        
        return required_data


    