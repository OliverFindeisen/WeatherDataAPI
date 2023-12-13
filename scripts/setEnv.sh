#!/bin/bash

export FLASK_APP=weatherapi.py # entry for flask
export DB_HOST=localhost # pg host
export DB_NAME=weather # pg database
export DB_USERNAME=weather # pg user
export DB_PASSWORD=test # pg password
export DB_TABLE_RESET=false # resets tables (true/false)