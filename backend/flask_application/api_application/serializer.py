#this methods are for organising the specific data that we need that can be later be used to save the data in the database
from dataclasses import dataclass


@dataclass
class WeekDataSerializer:
    location:str 
    weather_data : list
    


    def daily_data(self) -> dict:
        """
        this method iterates over the parsed data and returns a dict wi keys of the dates and values as the data
        """
        daily_dict = {}
        for days in self.weather_data:
            daily_dict[days["date"]] = {
                "hourly_data":days["hour"]}
        return daily_dict
    

    # def hourly_data(self):
    #     daily_dict = self.daily_data()
    #     hourly_filtered_data = {}
    #     # for dates in daily_dict:
            
    #     #     for hours in daily_dict[dates]["hourly_data"]:
    #     #         [items for items in hours]
    #     #         # hourly_filtered_data[dates] = {"data":{
    #     #         #     "hour":hours["time"],
    #     #         #     "will_it_rain" :hours["will_it_rain"],
    #     #         #     "chance_of_rain" :hours["chance_of_rain"],
    #     #         #     "wind_kph" :hours["wind_kph"],
    #     #         #     "feelslike_c" :hours["feelslike_c"],
    #     #         #     "temp_c" :hours["temp_c"],
    #     #         #     # "wind_dir" :hours["SE"],
    #     #         #     }}
    #     #         # print(hours)
    #     #         for items in hours:
    #     #             print(items)

    #     # print(hourly_filtered_data)
    #     print(type(daily_dict))
                






            #     "time":days["hour"]["time"],
            #     "is_day":days["hour"]["is_day"],
            #     "will_it_rain" :days["hour"]["will_it_rain"],
            #     "chance_of_rain" :days["hour"]["chance_of_rain"],
            #     "wind_kph" :days["hour"]["wind_kph"],
            #     "feelslike_c" :days["hour"]["feelslike_c"],
            #     "temp_c" :days["hour"]["temp_c"],
            #     "wind_dir" :days["hour"]["SE"],
            # }