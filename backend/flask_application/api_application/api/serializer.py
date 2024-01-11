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
    
