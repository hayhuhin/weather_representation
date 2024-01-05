import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry






# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
	# "latitude": 32.028320,
	# "longitude": 34.781879,


#TODO need a way to get the latitude and longitude of the users ip address

class OpenMeteoApi:
	def __init__(self,uri:str,params:dict,user_lat_lan:dict={}):
		self.uri = uri
		self.params = params
		self.user_lat_lan = user_lat_lan
		self.response = self.api_response()


	def api_response(self):
		responses = openmeteo.weather_api(self.uri, params=self.params)
		return responses[0]


	def get_daily_json(self):
		edited_params = {
			"hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
			"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
			"forecast_days":1,
							}
		hourly_responses = openmeteo.weather_api(self.uri,edited_params)

		hourly = hourly_responses.Hourly()
		hourly_precipitation_probability = hourly.Variables(0).ValuesAsNumpy()
		hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
		hourly_rain = hourly.Variables(2).ValuesAsNumpy()
		hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
		hourly_temperature_2m = hourly.Variables(4).ValuesAsNumpy()

		hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s"),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
		)}
		hourly_data["precipitation_probability"] = hourly_precipitation_probability
		hourly_data["rain"] = hourly_rain
		hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
		hourly_data["temperature_2m"] = hourly_temperature_2m
		hourly_data["feelslike_c"] = hourly_apparent_temperature


		hourly_dataframe = pd.DataFrame(data = hourly_data)
		return hourly_dataframe


	def get_week_json(self):

		# Process daily data. The order of variables needs to be the same as requested.
		daily = self.response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
		daily_showers_sum = daily.Variables(2).ValuesAsNumpy()
		daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
		daily_precipitation_probability_min = daily.Variables(4).ValuesAsNumpy()
		daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
		daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()


		daily_data = {"date": pd.date_range(
			start = pd.to_datetime(daily.Time(), unit = "s"),
			end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		)}

		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["temperature_2m_min"] = daily_temperature_2m_min
		daily_data["showers_sum"] = daily_showers_sum
		daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
		daily_data["precipitation_probability_min"] = daily_precipitation_probability_min
		daily_data["precipitation_hours"] = daily_precipitation_hours
		daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max


		daily_dataframe = pd.DataFrame(data = daily_data)
		print("daily",daily_dataframe)
		return daily_dataframe






API_2_CONFIG = {
    "uri":"https://api.open-meteo.com/v1/forecast",
    "key":"no key",
    "source":"openmateo api",
}

# #! ADD IT LATER INTO THE ENV 
# url = "https://api.open-meteo.com/v1/forecast"
API_2_PARAMS = {
    "past_days":7,
	"latitude": 32.028320,
	"longitude": 34.781879,
	"hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
	"forecast_days":1,
}



test_class = OpenMeteoApi(uri=API_2_CONFIG["uri"],params=API_2_PARAMS)
daily_data = test_class.get_daily_json()


for items in daily_data:
	print(daily_data[items])





# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below



# # url = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "past_days":7,
# 	"latitude": 32.028320,
# 	"longitude": 34.781879,
# 	"hourly": ["precipitation_probability", "apparent_temperature","rain", "wind_speed_10m", "temperature_2m"],
# 	"daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum","precipitation_probability_max","precipitation_probability_min","precipitation_hours", "wind_speed_10m_max"],
# 	"forecast_days":1,
# }


# responses = openmeteo.weather_api(url, params=params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
# # print(f"Elevation {response.Elevation()} m asl")
# # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
# # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_precipitation_probability = hourly.Variables(0).ValuesAsNumpy()
# hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
# hourly_rain = hourly.Variables(2).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
# hourly_temperature_2m = hourly.Variables(4).ValuesAsNumpy()

# hourly_data = {"date": pd.date_range(
# 	start = pd.to_datetime(hourly.Time(), unit = "s"),
# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
# 	freq = pd.Timedelta(seconds = hourly.Interval()),
# 	inclusive = "left"
# )}
# hourly_data["precipitation_probability"] = hourly_precipitation_probability
# hourly_data["rain"] = hourly_rain
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["feelslike_c"] = hourly_apparent_temperature


# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print(hourly_data)


# # Process daily data. The order of variables needs to be the same as requested.
# daily = response.Daily()
# daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
# daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
# daily_showers_sum = daily.Variables(2).ValuesAsNumpy()
# daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
# daily_precipitation_probability_min = daily.Variables(4).ValuesAsNumpy()
# daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
# daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()


# daily_data = {"date": pd.date_range(
# 	start = pd.to_datetime(daily.Time(), unit = "s"),
# 	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
# 	freq = pd.Timedelta(seconds = daily.Interval()),
# 	inclusive = "left"
# )}

# daily_data["temperature_2m_max"] = daily_temperature_2m_max
# daily_data["temperature_2m_min"] = daily_temperature_2m_min
# daily_data["showers_sum"] = daily_showers_sum
# daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
# daily_data["precipitation_probability_min"] = daily_precipitation_probability_min
# daily_data["precipitation_hours"] = daily_precipitation_hours
# daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max


# daily_dataframe = pd.DataFrame(data = daily_data)
# print("daily",daily_dataframe)
