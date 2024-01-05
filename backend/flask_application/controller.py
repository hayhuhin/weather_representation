
from api_application.redis_module import RedisConnector
from api_application.api_module import ApiCaller
from api_application.json_filter import JsonFilter
from api_application.graph_module import GraphRepresantation
from config import CURR_DIR,SECRET_FLASK_KEY,HOST_URI,REDIS_PORT,REDIS_USERNAME,REDIS_PASSWORD,WEATHERAPI_API_KEY,WEATHERAPI_API_URI


# redis_client = RedisConnector(host=HOST_URI,port=REDIS_PORT,username=REDIS_USERNAME,password=REDIS_PASSWORD)
api_connector = ApiCaller(uri=WEATHERAPI_API_URI,api_key=WEATHERAPI_API_KEY,source="weather_api")
graph_repr = GraphRepresantation()



class ControllerClass:
    def __init__(self,redis_config:dict,api_1_config:dict,api_2_config:dict=None,test_mode:bool=False):
        self.redis = RedisConnector(host=redis_config["host"],port=redis_config["port"],username=redis_config["username"],password=redis_config["password"])
        self.api_1 = ApiCaller(uri=api_1_config["uri"],api_key=api_1_config["key"],source=api_1_config["source"],test_mode=test_mode)
        # self.api_2 = ApiCaller(uri=api_2_config["uri"],api_key=api_2_config["key"],source=api_2_config["source"])
        self.graph_repr = GraphRepresantation()
        self.json = JsonFilter



    def ft_time(self,start_date,ip):
        cleaned_data = {
            "start_date":start_date,
            "end_date":start_date,
            "ip":ip,
        }

        #this is only for the api_1 getting data
        api_data = self.api_1.weather_by_range(request_data=cleaned_data)

        json_filter_class = self.json(json_data=api_data)

        #this is for filtering the data into day repr
        filtered_api_data = json_filter_class.specific_day_data(date=start_date)

        #ths adding additional graph_repr key with day value
        # filtered_api_data[0]["graph_repr"] = "day"

        #this adding the cache data into the redis db
        result = self.redis.set_key(key=ip,value={"user_data":filtered_api_data,"graph_repr":"day"})
        
        #this getting the new data key from redis
        required_data = self.redis.get(key=ip)

    
    def change_state(self,state,start,end,ip):
        #first we checking if the user already sended api_1 request in the last 30 sec
        timer_is_set = self.redis.check_timer(key=ip)
        if timer_is_set:
            print("you have ttl ")
            return {"error":"you have ttl for the query"}


        if state == "week":

            cleaned_data = {
            "start_date":start,
            "end_date":end,
            "ip":ip,
            }
            api_data = self.api_1.weather_by_range(cleaned_data)
            json_filter_class = self.json(json_data=api_data)



            #this is for filtering the data into day repr
            filtered_api_data = json_filter_class.specific_week_data(start_date=start ,end_date=end)
            print(filtered_api_data)
            print(state,start,end,ip)
            #ths adding additional graph_repr key with day value
            # filtered_api_data["graph_repr"] = "week"

            #first we delete the existing data if any
            delete_user = self.redis.clear_all(ip)

            #this adding the cache data into the redis db

            self.redis.set_key(key=ip,value={"user_data":filtered_api_data,"graph_repr":"week"},timer=15)
            
            #this getting the new data key from redis
            # required_data = self.redis.get(key=ip)


            # weather_graph = self.week_view(required_data)
            # return required_data
        
        if state == "day":
            print("im here")
            cleaned_data = {
            "start_date":start,
            "end_date":start,
            "ip":ip,
            }
            api_data = self.api_1.weather_by_range(cleaned_data)
            json_filter_class = self.json(json_data=api_data)

            #this is for filtering the data into day repr
            filtered_api_data = json_filter_class.specific_day_data(date=start)

            #ths adding additional graph_repr key with day value
            # filtered_api_data["graph_repr"] = "day"
            
            #first we delete the existing data if any
            delete_user = self.redis.clear_all(ip)

            #this adding the cache data into the redis db
            result = self.redis.set_key(key=ip,value={"user_data":filtered_api_data,"graph_repr":"day"},timer=15)

            
            #this getting the new data key from redis
            # required_data = self.redis.get(key=ip)
            # print(required_data)
            # weather_day_graph = self.day_view(required_data=required_data)
            # return weather_day_graph
        

    def day_view(self,required_data) -> str:
        # required_data = self.redis.get(key=self.ip)

        temp_c = required_data["user_data"][0]
        will_it_rain = required_data["user_data"][1]
        chance_of_rain = required_data["user_data"][2]
        wind_kph = required_data["user_data"][3]
        feelslike_c = required_data["user_data"][4]
        source = required_data["user_data"][5]


        # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
        temp_c_html = self.graph_repr.graph_options(graph_type="line_graph",dict_values=temp_c,graph_repr="1_row",path="")
        will_it_rain_html= self.graph_repr.graph_options(graph_type="line_graph",dict_values=will_it_rain,graph_repr="1_row",path="")
        chance_of_rain_html = self.graph_repr.graph_options(graph_type="line_graph",dict_values=chance_of_rain,graph_repr="1_row",path="")
        wind_kph_html = self.graph_repr.graph_options(graph_type="line_graph",dict_values=wind_kph,graph_repr="1_row",path="")
        feelslike_c_html = self.graph_repr.graph_options(graph_type="line_graph",dict_values=feelslike_c,graph_repr="1_row",path="")




        weather_day_graph = {
            "temp_c":{"html":temp_c_html,"data":{"name":"temperature","appearance":[f"blue bar is {source['blue_bar']}",f"red bar is {source['red_bar']}"]}},
            "will_it_rain":{"html":will_it_rain_html,"data":{"name":"will it rain","appearance":[f"blue bar is {source['blue_bar']}",f"red bar is {source['red_bar']}"]}},
            "chance_of_rain":{"html":chance_of_rain_html,"data":{"name":"chance of rain","appearance":[f"blue bar is {source['blue_bar']}",f"red bar is {source['red_bar']}"]}},
            "wind_kph":{"html":wind_kph_html,"data":{"name":"wind kph","appearance":[f"blue bar is {source['blue_bar']}",f"red bar is {source['red_bar']}"]}},
            "feelslike_c":{"html":feelslike_c_html,"data":{"name":"feels like ","appearance":[f"blue bar is {source['blue_bar']}",f"red bar is {source['red_bar']}"]}},
                            }

        return weather_day_graph


    def week_view(self,required_data):

        #must be fixed because there is no realy graph is needed and only cards
        #to display the different weathers
        # redis_dict = self.redis.get(key=self.ip)
        #*this dict is store as a nested dict 
        #*main key is {date:{"maxtemp":"10","mintemp":-10}}
        
        return required_data


    