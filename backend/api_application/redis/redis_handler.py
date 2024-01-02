import redis,json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path="backend/api_application/.env")

class RedisConnector:
  def __init__(self,host,port,username,password):
    self.collection = redis.Redis(host=host,port=port,username=username,password=password)

  def register_ip(self):
    pass


host = os.environ.get("REDIS_HOST_URI")
port = os.environ.get("REDIS_PORT")
username = os.environ.get("REDIS_USERNAME")
password = os.environ.get("REDIS_PASSWORD")

test_redis = RedisConnector(host=host,port=port,username=username,password=password)

