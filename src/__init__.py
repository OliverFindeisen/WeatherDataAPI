import os
from src.helper.dbconnector import DbConnector
from flask import Flask
from src import weather_routes

app = Flask(__name__, instance_relative_config=True)
reset = False
if os.environ['DB_TABLE_RESET'] == "true":
    reset = True

print("init")
DbConnector.init(DbConnector, reset)

# create and configure the src
app.config.from_pyfile("../resources/config.py")
app.register_blueprint(weather_routes.routes)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# a simple page that says hello

