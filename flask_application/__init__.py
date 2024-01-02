from flask_caching import Cache
from flask import Flask
import redis,os
from dotenv import load_dotenv
load_dotenv(dotenv_path="backend/api_application/.env")

#redis first setup 
host_uri = os.environ.get("REDIS_HOST_URI")
port = os.environ.get("REDIS_PORT")
username = os.environ.get("REDIS_USERNAME")
password = os.environ.get("REDIS_PASSWORD")



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = host_uri
    app.config['CACHE_REDIS_PORT'] = port
    app.config['CACHE_REDIS_DB'] = 0
    app.config['REDIS_USERNAME'] = username
    app.config['REDIS_PASSWORD'] = password

    # Initialize Flask-Caching with Redis
    cache = Cache(app=app)
    cache.init_app(app)

    # Initialize Redis client
    redis_client = redis.Redis(host=host_uri, port=port, db=0,username=username,password=password)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app