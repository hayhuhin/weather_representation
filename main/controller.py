from infrastructure.modules.redis_module import RedisConnector
from infrastructure.modules.graph_module import GraphRepresantation
from infrastructure.api.adapter import ApiFacade


class ControllerClass:
    def __init__(self,redis_config:dict,test_mode:bool=False):
        self.redis = RedisConnector(host=redis_config["host"],port=redis_config["port"],username=redis_config["username"],password=redis_config["password"])
        self.api_facade = ApiFacade()
        self.graph_repr = GraphRepresantation()
        self.user_ttl = redis_config["user_ttl"]
        self.api_ttl = redis_config["api_ttl"]




        #initialising the day requests and the week requests
        self.initialised_apis = self.api_facade.register_api_methods()
        

    def first_time(self,start_date,end_date,ip) -> None:
        params = {
            "start_date":start_date,
            "end_date":end_date,
            "ip":ip,
        }


        #*creating the request from the api's and then getting the data
        day_data = self.api_facade.get_day_request(params=params)

        #this adding the cache data into the redis db
        result = self.redis.set_key(key=ip,value={"user_data":day_data,"graph_repr":"day"})

    
    def change_state(self,state:str,start_date:str,end_date:str,ip:str) -> None:
        #first we checking if the user already sent api request in the last 30 sec

        #!need to have another class that have the current state of the application
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
            
            week_data = self.api_facade.get_week_request(params=params)

            #first we delete the existing data if any
            self.redis.clear_all(ip)

            #this adding the cache data into the redis db
            self.redis.set_key(key=ip,value={"user_data":week_data,"graph_repr":"week"},timer=self.api_ttl)
            
        
        if state == "day":

            params = {
            "start_date":start_date,
            "end_date":start_date,
            "ip":ip,
            }            
            #first we delete the existing data if any
            self.redis.clear_all(ip)

            #this adding the cache data into the redis db
            day_data = self.api_facade.get_day_request(params=params)
            result = self.redis.set_key(key=ip,value={"user_data":day_data,"graph_repr":"day"},timer=self.api_ttl)
        

    def day_view(self,required_data,graph_type:str="line_graph_compared") -> dict:


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


        openmateo_min_max = required_data["user_data"]["openmateo"]["openmateo_min_max"]
        weatherapi_min_max = required_data["user_data"]["weatherapi"]["weatherapi_min_max"]



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


    def week_view(self,required_data) ->dict:

        return required_data


    