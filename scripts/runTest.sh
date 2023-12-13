#!/bin/bash

echo "Auto run tests"

echo "Run Test A with the values cityname berlin and date 2021-12-14"
read -p "Press any key to continue... " -n1 -s
curl -s "localhost:8088/endpointa?cityname=berlin&datestring=2021-12-14" | jq .

echo "Run Test B with the values cityname athens and month 10"
read -p "Press any key to continue... " -n1 -s
curl -s "localhost:8088/endpointb?cityname=athens&month=10" | jq .

echo "Run Test C with the values cityname berlin and date 2021-10-13"
read -p "Press any key to continue... " -n1 -s
curl -s "localhost:8088/endpointc?cityname=berlin&datestring=2021-10-13" | jq .

echo "Run Test D with the values cityname athens and year 2015"
read -p "Press any key to continue... " -n1 -s
curl -s "localhost:8088/endpointd?cityname=athens&year=2015"  | jq .