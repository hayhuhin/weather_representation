import os
from datetime import timedelta

import redis
from flask import Flask, render_template_string, request, session, jsonify,render_template,redirect, url_for

from dotenv import load_dotenv
CURR_DIR = os.path.dirname(os.path.abspath(__file__))


load_dotenv(dotenv_path=r"C:\Users\hayhuhin\Desktop\weather_web\backend\api_application\.env")


#environment variables
host_uri = os.environ.get("REDIS_HOST_URI")
port = os.environ.get("REDIS_PORT")
username = os.environ.get("REDIS_USERNAME")
password = os.environ.get("REDIS_PASSWORD")


#flass app configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['REDIS_USERNAME'] = username
app.config['REDIS_PASSWORD'] = password
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(f'redis://{host_uri}')


#TODO need to add class that accepts the ip and returns json data by the location
@app.route("/main",methods=["GET"])
def intro_page():
      user_ip = request.remote_addr
      if  user_ip in  session:
            return render_template("main.html",content=user_ip)


@app.route('/weather', methods=['GET'])
def weather_info():
      return jsonify({'message': 'Item added successfully'})


if __name__ == "__main__":
     
      app.secret_key = 'super secret key'

      app.debug = True
      app.run()

