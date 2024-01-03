import os,json
from datetime import timedelta
from flask import Flask, render_template_string, request, session, jsonify,render_template,redirect, url_for
from dotenv import load_dotenv
from redis_application.redis_handler import RedisConnector
from api_application.api_caller import ApiCaller,JsonFilter
from plotly_application.graph_presentation import GraphRepresantation
from view import ViewClass


CURR_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=CURR_DIR+"/configuration/.env")




#! TESTING ONLY
#! testing only
#mock data that used to have json data to use
# json_filter_class = None
# mock_data = None
# #*this created to work with JsonFilter class
# with open(CURR_DIR+"/api_application/mock_data.json","r") as json_file:
#     json_data = json.load(json_file)
#     json_filter_class = JsonFilter(json_data=json_data)
#     mock_data = json_filter_class.specific_day_data(date="2024-01-01")

# print(mock_data)

#environment variables
host_uri = os.environ.get("REDIS_HOST_URI")
port = os.environ.get("REDIS_PORT")
username = os.environ.get("REDIS_USERNAME")
password = os.environ.get("REDIS_PASSWORD")

#api env
api_uri = os.environ.get("API_URI")
api_key = os.environ.get("API_KEY")


#flass app configuration and initialisation
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_FLASK_KEY')

#class instances for api,db,html representation
redis_client = RedisConnector(host=host_uri,port=port,username=username,password=password)
api_connector = ApiCaller(uri=api_uri,api_key=api_key,source="weather_api")
graph_repr = GraphRepresantation()
view = ViewClass(redis=redis_client,api=api_connector,graph=graph_repr,ip=request.remote_addr,json=JsonFilter)



#TODO add function that accepts the user ip and return the api call that passed later into 
#TODO representation class 
@app.route("/homepage",methods=["GET"])
def home_page():
    #user ip address
    user_ip = request.remote_addr
    #checking if the key is already exists
    found_key = redis_client.exists(key=user_ip)

    if found_key:
        return render_template("home.html")
    #if the key not exists then creating one with the default TTL 
    else:
        
        #default values
        start = "2024-01-04"
        end = "2024-01-05"
        ip = request.remote_addr
        sorted_by = "daily"

        #basic dict to pass into the api class
        cleaned_data = {
            "start_date":start,
            "end_date":end,
            "ip":"8.8.8.8",
        }

        #querying the api and saving the response json
        json_response = api_connector.weather_by_range(request_data=cleaned_data)
        #getting the specific data needed from the api call

        json_filter = JsonFilter(json_data=json_response)

        day_weather_data = json_filter.specific_day_data(date=start)
        #this adding the cache data into the redis db

        result = redis_client.set_key(key=user_ip,value={"content_data":day_weather_data})
        return render_template("home.html")



@app.route('/weather', methods=['GET','POST'])
def weather_info():
    #user ip address
    if request.method == "GET":
        user_ip = request.remote_addr
        #checking if the key is already exists
        found_key = redis_client.exists(key=user_ip)

        #the user is already have data in redis
        if found_key:
            required_data = redis_client.get(key=request.remote_addr)

            

            #first im calling the api and passing the data into JsonFilter class that filtering the data into more specific needed data
            #this specific data passed into the plotly graph repr and saved as html that passed into the user content
            #* need to add start as today end as future by week
            start = "2024-01-01"
            end = "2024-01-01"
            ip = request.remote_addr
            sorted_by = "daily"
            cleaned_data = {
                "start_date":start,
                "end_date":end,
                "ip":ip,
                "sorted_by":sorted_by
            }
            #querying the api and saving the response json
            # json_response = api_connector.weather_by_range(request_data=cleaned_data)
            #getting the specific data needed from the api call
            api_data = api_connector.weather_by_range(request_data=cleaned_data)
            json_filter = JsonFilter(json_data=api_data)
            default_view = json_filter.specific_day_data(date=start)
            #this adding the cache data into the redis db
            result = redis_client.set_key(key=user_ip,value={"user_data":default_view})
            #the gathered data from the users redis
            required_data = redis_client.get(key=request.remote_addr)



            for time in required_data["user_data"]:
                
                x.append(time)
                y.append(int(required_data["user_data"][time]["temp_c"]))

            dict_values= {"x":x,"y":y,"y_2":[]}
            graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")



            #*for testing only
            return render_template("weather.html",content={"graph_html":graph_html})
        


            # return render_template("weather.html",content=f"user already exists{user_ip}")
            #if the key not exists then creating one with the default TTL 
       
       
       
        else:
            if required_data["weather_repr"] == "day":
                #the data structured in a way that the graph_html can proccess it
                temp_c = required_data["content_data"][0]
                will_it_rain = required_data["content_data"][1]
                chance_of_rain = required_data["content_data"][2]
                wind_kph = required_data["content_data"][3]
                feelslike_c = required_data["content_data"][4]

                # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
                temp_c_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=temp_c,graph_repr="1_row",path="")
                will_it_rain_html= graph_repr.graph_options(graph_type="bar_graph",dict_values=will_it_rain,graph_repr="1_row",path="")
                chance_of_rain_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=chance_of_rain,graph_repr="1_row",path="")
                wind_kph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=wind_kph,graph_repr="1_row",path="")
                feelslike_c_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=feelslike_c,graph_repr="1_row",path="")

                weather_graph = {
                    "temp_c_html":temp_c_html,
                    "will_it_rain_html":will_it_rain_html,
                    "chance_of_rain_html":chance_of_rain_html,
                    "wind_kph_html":wind_kph_html,
                    "feelslike_c_html":feelslike_c_html
                }
                return render_template("weather.html",content=weather_graph)



            #! working on for now this section is not valid
            #it will represent it as a day 
            elif required_data["weather_repr"] == "week":
                temp_c = required_data["content_data"][0]
                will_it_rain = required_data["content_data"][1]
                chance_of_rain = required_data["content_data"][2]
                wind_kph = required_data["content_data"][3]
                feelslike_c = required_data["content_data"][4]

                # graph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=dict_values,graph_repr="1_row",path="")
                temp_c_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=temp_c,graph_repr="1_row",path="")
                will_it_rain_html= graph_repr.graph_options(graph_type="bar_graph",dict_values=will_it_rain,graph_repr="1_row",path="")
                chance_of_rain_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=chance_of_rain,graph_repr="1_row",path="")
                wind_kph_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=wind_kph,graph_repr="1_row",path="")
                feelslike_c_html = graph_repr.graph_options(graph_type="bar_graph",dict_values=feelslike_c,graph_repr="1_row",path="")

                weather_graph = {
                    "temp_c_html":temp_c_html,
                    "will_it_rain_html":will_it_rain_html,
                    "chance_of_rain_html":chance_of_rain_html,
                    "wind_kph_html":wind_kph_html,
                    "feelslike_c_html":feelslike_c_html
                }

                return render_template("weather.html",content=weather_graph)


        
        
    if request.method == "POST":
        user_ip = request.user
        user_key = redis_client.get(key=request.remote_addr)
        print(request.POST)
        return redirect("/weather")

#this section is the buttons that ill have to change the repr of the page




if __name__ == "__main__":
    app.secret_key = os.getenv('SECRET_FLASK_KEY')
    app.debug = True
    app.run()
