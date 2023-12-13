#!/bin/bash

curl -X POST -F cityname=athens -F file=@resources/weather-athens.csv localhost:8088/upload
curl -X POST -F cityname=berlin -F file=@resources/weather-berlin.csv localhost:8088/upload