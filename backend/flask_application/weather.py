import os,json
from datetime import timedelta,date,datetime
from flask import Flask, render_template_string, request, session, jsonify,render_template,redirect, url_for
from dotenv import load_dotenv
from redis_application.redis_handler import RedisConnector
from api_application.api_caller import ApiCaller,JsonFilter
from plotly_application.graph_presentation import GraphRepresantation
from view import ViewClass

#env and directory setup
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=CURR_DIR+"/configuration/.env")

#datetime setup
today = str(date.today())
week_dates = []
format_dates = datetime.strptime(today,"%Y-%m-%d")
for i in range(1,8):
    week_dates.append(str(format_dates+timedelta(days=-i))[:10:])







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
view = ViewClass(redis=redis_client,api=api_connector,graph=graph_repr)



#TODO add function that accepts the user ip and return the api call that passed later into 
#TODO representation class 
@app.route("/homepage",methods=["GET"])
def home_page():
    #user ip address
    # user_ip = request.remote_addr#! uncomment in prod
    user_ip = "8.8.8.8"

    #checking if the key is already exists
    found_key = redis_client.exists(key=user_ip)

    if found_key:
        return render_template("home.html")
    #if the key not exists then creating one with the default TTL 
    else:
        view.ft_time(start_date=week_dates[0],ip=user_ip)
        return render_template("home.html")



@app.route('/weather', methods=['GET'])
def weather_info():


    end = week_dates[-1]
    start = week_dates[0]
    #user ip address
    if request.method == "GET":
        # user_ip = request.remote_addr#! uncomment it in prod
        user_ip = "8.8.8.8"

        #checking if the key is already exists
        user_exists = redis_client.exists(key=user_ip)

        #the user is already have data in redis
        if user_exists:
            api_data = redis_client.get(key=user_ip)

            current_state = redis_client.get(key=user_ip)["graph_repr"]
            if current_state == "day":
                # weather_day_graph = view.change_state(state="day",start=start,end=end,ip=user_ip)
                weather_day_graph = view.day_view(required_data=api_data) 
                #*for testing only
                return render_template("weather.html",content={"weather_day_graph":weather_day_graph})

            if current_state == "week":
                # week_data = view.change_state(state="week",start=start,end=end,ip=user_ip)
                week_data = view.week_view(required_data=api_data)
                #*for testing only

                return render_template("weather.html",content={"week_data":week_data})


       
        else:
            view.ft_time(start_date=start,ip=user_ip)
            api_data = redis_client.get(key=user_ip)
            weather_day_graph = view.day_view(required_data=api_data) 
            return render_template("weather.html",content={"weather_day_graph":weather_day_graph})



@app.route('/weather/day',methods=["GET"])
def display_day():
    user_ip = "8.8.8.8"
    view.change_state(state="day",start=week_dates[-1],end=week_dates[0],ip=user_ip)
    return redirect(url_for('weather_info'))
    



@app.route('/weather/week',methods=["GET"])
def display_week():
    user_ip = "8.8.8.8"
    view.change_state(state="week",start=week_dates[-1],end=week_dates[0],ip=user_ip)
    return redirect(url_for('weather_info'))
    
    

    # if request.method == "POST":

    #     user_ip = "8.8.8.8"
    #     if request.values.get("change_display") == "day":
    #         view.change_state(state="day",start=start,end=end,ip=user_ip)
    #         return redirect("/weather")
        
    #     if request.values.get("change_display") == "week":
    #         view.change_state(state="week",start=start,end=end,ip=user_ip)
    #         return redirect("/weather")
        
#this section is the buttons that ill have to change the repr of the page


# redis_client.clear_all("127.0.0.1")
# redis_client.clear_all("8.8.8.8")
# redis_client.get(key="127.0.0.1")
# redis_client.get(key="8.8.8.8")

if __name__ == "__main__":
    app.secret_key = os.getenv('SECRET_FLASK_KEY')
    app.debug = True
    app.run()
