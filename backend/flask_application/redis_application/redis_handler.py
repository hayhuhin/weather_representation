import redis,json,os
from dotenv import load_dotenv
from redis.commands.json.path import Path

load_dotenv(dotenv_path="backend/api_application/.env")

class RedisConnector:
  """"
  wrapper class that uses redis methods that later used in the main applicatin
  
  """

  def __init__(self,host,port,username,password):
    self.collection = redis.Redis(host=host,port=port,username=username,password=password)

  def register_ip(self):
    pass


  def set_key(self,key:str,value:dict,replace:bool=False,TTL:int=3600) -> bool:
    """
    setting the key in the redis database

    ARGS:
      key(str):the users key that saved
      value(dict):this is the data itself and it must be a dict so the data will look like this:
        dict = {"value_key":"the value itself"}
      replace(bool=False):if true it will replace the existing data
      TTL(int=3600):time to live and its the timer that the key will be destroyed after the time expires
    """
    
    #check if the key exists
    if self.exists(key=key):
      #if replace true it will replace the existing data
      if replace:
        self.collection.set(key,value)
        return True
      #handles that the bool is inapropriate
      return ValueError("the user is already have record and replace set to false")

    value["weather_repr"] = "week"
    #saving the wanted data in the redis database
    self.collection.json().set(key,Path.root_path(),value)
    #creating expiration date for the key
    self.collection.expire(key,TTL)  
    #returns True that the key is created
    return True
  


  def get(self,key:str,specific_value:str=None) -> bool:
    """
    this get method is similar to redis.get method but returns false if data not found

    ARGS:
      key(str):key that saved in the redis db
      specific_value(str): can pass specific nested dicts and it will return the specific data 
        for example: 'data.time' and it will return the nested dict of data
    
    Returns:
      if key not found will return false and if key exists will return its data
    """

    #if i passed any value specific field
    if specific_value:
      result = self.collection.json().get(key,specific_value)  

    #if specific values not passed
    result = self.collection.json().get(key)
    
    #checkinf if anything is found
    if result == None:
      return False
    return result
  


  def exists(self,key:str) -> bool:
    """
    checking if the key exists and will return boolean

    Returns:
      true if exists. false if not exists
    """
    result = self.collection.exists(key)
    if result:
      return True
    return False
    # return result

  def clear_all(self,ip:str):
    """
    this method is specific for testing and it deletes the specified key
    """
    self.collection.delete(ip)



