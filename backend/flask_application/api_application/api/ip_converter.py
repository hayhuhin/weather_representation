import requests







class IpConverter:
    def __init__(self,api_key,ip_addr):
        self.api_key = api_key
        self.ip = ip_addr


    def queue_micro_service(self):
        print("ip api called")
        
        return True
    

    def geo_location(self):
        if self.queue_micro_service:
            
            query = f'https://api.ipgeolocation.io/timezone?apiKey={self.api_key}&ip={self.ip}'
            
            geo_data = {}
            latitude_api_data = requests.get(query).json()["geo"]["latitude"]
            longitude_api_data = requests.get(query).json()["geo"]["longitude"]

            geo_data["latitude"] = latitude_api_data
            geo_data["longitude"] = longitude_api_data

            return geo_data

