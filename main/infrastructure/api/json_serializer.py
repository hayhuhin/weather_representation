"""
    helper functions that build specificly for weatherapi API 
    that handles and reconstructing the retrieved json from the API call 
    and returns structured data
"""


def filltered_week_json(retrieved_json:dict) -> dict:
    """
    simple function that build specificly for the weather api that reconstructs 
    the API json into something that we can use in our application
    this specific method is returning the week json data
    Args:
        retirieved_json(dict):
            as the name says it its the retrieved API json data

    Returns:
        week json data
    """


    filtered_data = {}
    for data in retrieved_json["forecast"]["forecastday"]:
        filtered_data[data["date"]] = {
            "maxtemp_c":data["day"]["maxtemp_c"],
            "mintemp_c":data["day"]["mintemp_c"],
            "avgtemp_c":data["day"]["avgtemp_c"],
            "daily_will_it_rain":data["day"]["daily_will_it_rain"],
            "daily_chance_of_rain":data["day"]["daily_chance_of_rain"],
        }

    return filtered_data


def filltered_day_json(retrieved_json:dict,targeted_day:dict) -> dict:
    """
    simple function that build specificly for the weather api that reconstructs 
    the API json into something that we can use in our application
    this specific method is returning the  hourly json data
    Args:
        retirieved_json(dict):
            as the name says it its the retrieved API json data
        targeted_day(dict):
            the specific day that we want to get the hourly data

    Returns:
        hourly data by the specific date as Json
    """

    #first we are creating a dict by hours when iterating over the json
    weather_data = retrieved_json["forecast"]["forecastday"]
    daily_dict = {}
    for days in weather_data:
        daily_dict[days["date"]] = {
            "hourly_data":days["hour"]}

    #then reconstructing and formatting dict with the needed data to  
    #be parsed into weather app
    hourly_dict = {}
    for items in daily_dict[targeted_day]["hourly_data"]:

        hourly_dict[items["time"][-5::]] = {
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


    dict_data = {"temp_c":temp_c,"will_it_rain":will_it_rain,"chance_of_rain":chance_of_rain,"wind_kph":wind_kph,"feelslike_c":feelslike_c}

    return dict_data


