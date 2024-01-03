class ViewClass:
    def __init__(self,redis,api,graph,ip,json):
        self.redis = redis
        self.api = api
        self.graph_repr = graph
        self.ip = ip
        self.json = json



    def ft_time(self,start_date):
        cleaned_data = {
            "start_date":start_date,
            "end_date":start_date,
            "ip":self.ip,
        }

        #this is only for the api getting data
        api_data = self.api.weather_by_range(request_data=cleaned_data)
        json_filter_class = self.json(json_data=api_data)

        #this is for filtering the data into day repr
        filtered_api_data = json_filter_class.specific_day_data(date=start_date)

        #ths adding additional graph_repr key with day value
        filtered_api_data["graph_repr"] = "day"

        #this adding the cache data into the redis db
        result = self.redis.set_key(key=self.ip,value={"user_data":filtered_api_data})
        
        #this getting the new data key from redis
        required_data = self.redis.get(key=self.ip)

    
    def change_state(self,state,start,end):
        if state == "week":

            cleaned_data = {
            "start_date":start,
            "end_date":end,
            "ip":self.api,
            }
            api_data = self.api.weather_by_range(cleaned_data)
            json_filter_class = self.json(json_data=api_data)

            #this is for filtering the data into day repr
            filtered_api_data = json_filter_class.specific_week_data(start_date=start ,end_date=end)

            #ths adding additional graph_repr key with day value
            filtered_api_data["graph_repr"] = "week"

            #this adding the cache data into the redis db
            result = self.redis.set_key(key=self.ip,value={"user_data":filtered_api_data})
            
            #this getting the new data key from redis
            required_data = self.redis.get(key=self.ip)

            view = self.week_view(required_data)
            return view
        
        if state == "day":

            cleaned_data = {
            "start_date":start,
            "end_date":start,
            "ip":self.api,
            }
            api_data = self.api.weather_by_range(cleaned_data)
            json_filter_class = self.json(json_data=api_data)

            #this is for filtering the data into day repr
            filtered_api_data = json_filter_class.specific_day_data(start_date= start)

            #ths adding additional graph_repr key with day value
            filtered_api_data["graph_repr"] = "day"

            #this adding the cache data into the redis db
            result = self.redis.set_key(key=self.ip,value={"user_data":filtered_api_data})
            
            #this getting the new data key from redis
            required_data = self.redis.get(key=self.ip)
            return required_data
        



    def day_view(self) -> str:
        required_data = self.redis.get(key=self.ip)
        temp_c = required_data["content_data"][0]
        will_it_rain = required_data["content_data"][1]
        chance_of_rain = required_data["content_data"][2]
        wind_kph = required_data["content_data"][3]
        feelslike_c = required_data["content_data"][4]

        # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
        temp_c_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=temp_c,graph_repr="1_row",path="")
        will_it_rain_html= self.graph_repr.graph_options(graph_type="bar_graph",dict_values=will_it_rain,graph_repr="1_row",path="")
        chance_of_rain_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=chance_of_rain,graph_repr="1_row",path="")
        wind_kph_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=wind_kph,graph_repr="1_row",path="")
        feelslike_c_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=feelslike_c,graph_repr="1_row",path="")

        weather_graph = {
            "temp_c_html":temp_c_html,
            "will_it_rain_html":will_it_rain_html,
            "chance_of_rain_html":chance_of_rain_html,
            "wind_kph_html":wind_kph_html,
            "feelslike_c_html":feelslike_c_html
        }

        return weather_graph

# cleaned_data = {
#     "start_date":start,
#     "end_date":end,
#     "ip":ip,
#     "sorted_by":sorted_by
# }
# api_data = api_connector.weather_by_range(request_data=cleaned_data)
# json_filter = JsonFilter(json_data=api_data)
# default_view = json_filter.specific_day_data(date=start)
# #this adding the cache data into the redis db
# result = redis_client.set_key(key=user_ip,value={"user_data":default_view})
# #the gathered data from the users redis
# required_data = redis_client.get(key=request.remote_addr)







    def week_view(self):

        #must be fixed because there is no realy graph is needed and only cards
        #to display the different weathers
        redis_dict = self.redis.get(key=self.ip)
        #*this dict is store as a nested dict 
        #*main key is {date:{"maxtemp":"10","mintemp":-10}}

        #TODO need a way to repr the data as html or pass it in some way

        # # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
        # temp_c_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=temp_c,graph_repr="1_row",path="")
        # feelslike_c_html = self.graph_repr.graph_options(graph_type="bar_graph",dict_values=feelslike_c,graph_repr="1_row",path="")

        # weather_graph = {
        #     "temp_c_html":temp_c_html,
        #     "feelslike_c_html":feelslike_c_html
        # }
        
        # return weather_graph
