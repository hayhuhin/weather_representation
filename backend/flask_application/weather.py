import os,json
from flask import Flask, render_template_string, request, session, jsonify,render_template,redirect, url_for
from api_application.datetimes_module import Time
from controller import ControllerClass
from config import SECRET_FLASK_KEY,REDIS_CONFIG,API_1_CONFIG



#flass app configuration and initialisation

app = Flask(__name__)
app.secret_key = SECRET_FLASK_KEY


controller = ControllerClass(redis_config=REDIS_CONFIG,api_1_config=API_1_CONFIG,test_mode=True)

week_dates =  Time().week_reversed()


@app.route("/homepage",methods=["GET"])
def home_page():
    #user ip address
    # user_ip = request.remote_addr#! uncomment in prod
    user_ip = "8.8.8.8"

    #checking if the key is already exists
    found_key = controller.redis.exists(key=user_ip)

    if found_key:
        return render_template("home.html")
    #if the key not exists then creating one with the default TTL 
    else:
        controller.ft_time(start_date=week_dates[0],ip=user_ip)
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
        user_exists = controller.redis.exists(key=user_ip)

        #the user is already have data in redis
        if user_exists:
            api_data = controller.redis.get(key=user_ip)

            current_state = controller.redis.get(key=user_ip)["graph_repr"]
            if current_state == "day":
                # weather_day_graph = controller.change_state(state="day",start=start,end=end,ip=user_ip)
                weather_day_graph = controller.day_view(required_data=api_data) 
                #*for testing only
                return render_template("weather.html",content={"weather_day_graph":weather_day_graph})

            if current_state == "week":
                # week_data = controller.change_state(state="week",start=start,end=end,ip=user_ip)
                week_data = controller.week_view(required_data=api_data)
                #*for testing only

                return render_template("weather.html",content={"week_data":week_data})


       
        else:
            controller.ft_time(start_date=start,ip=user_ip)
            api_data = controller.redis.get(key=user_ip)
            weather_day_graph = controller.day_view(required_data=api_data) 
            return render_template("weather.html",content={"weather_day_graph":weather_day_graph})



@app.route('/weather/day',methods=["GET"])
def display_day():
    user_ip = "8.8.8.8"
    controller.change_state(state="day",start=week_dates[-1],end=week_dates[0],ip=user_ip)
    return redirect(url_for('weather_info'))



@app.route('/weather/week',methods=["GET"])
def display_week():
    user_ip = "8.8.8.8"
    controller.change_state(state="week",start=week_dates[-1],end=week_dates[0],ip=user_ip)
    return redirect(url_for('weather_info'))
    

if __name__ == "__main__":
    app.secret_key = os.getenv('SECRET_FLASK_KEY')
    app.debug = True
    app.run()
