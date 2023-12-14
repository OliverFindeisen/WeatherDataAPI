# WeatherdataAPI

## Task description

Weather data API

The goal of this project is to create an API that serves historical weather information and statistics. The
historical weather information for each city will be provided in a file. 
The file contains:

The timestamp of the weather information (granularity is hour).
The average temperature 2m above ground (in Celcius).
Rain and snow (mm) for that hour.
One file (CSV) for each city will be used. Please find attached two example CSV files for Berlin and
Athens.
Deliverables

The following must be part of the solution.

Scripts to import data to a Postgres database.
A service with the following endpoints:
- An endpoint to get all available weather information for a given city and date.
- An endpoint to get the number of days with rain for a given city and month.
- An endpoint to get the number of days since it last rained for a given city and date.
- An endpoint to provide the number of days it rained, the number of days it was snowed
and the number of days with extreme heat (temperature was > 30 C sometime during
the day) for a given year and city.
Please provide a .zip file or access to a private git repo containing:

The source code.
Instructions on how to setup, run and access the endpoints.
Anything else that you consider important.

## USAGE 

## requirements


Script output are formated with jq
`sudo apt-get install jq`

- GIT
Private repository access with e.g. id_rsa.pub

- POSTGRES
- database/user/password set see ENV below
- pg.hba configured for local


## Install 

- `mkdir <some/folder>`
- `cd <some/folder>`
- `git clone git@github.com:OliverFindeisen/WeatherDataAPI.git`
- `git checkout master`
- `python3 -m venv api`
- `source api/bin/activate`
- `pip install -r requirements.txt`

## add required ENV

- `export FLASK_APP=weatherapi.py` # entry for flask
- `export DB_HOST=localhost` # pg host
- `export DB_NAME=weather` # pg database
- `export DB_USERNAME=weather` # pg user
- `export DB_PASSWORD=test` # pg password
- `export DB_TABLE_RESET=false` # resets tables (true/false)

these values can be applied via `source scripts/setEnv.sh`

## Start

- `flask run --port=8088`

## open new terminal to start requests

### Upload

- `curl -X POST -F cityname=athens -F file=@resources/weather-athens.csv localhost:8088/upload`
- `curl -X POST -F cityname=berlin -F file=@resources/weather-berlin.csv localhost:8088/upload`
### Endpoint Requests Auto

- `./scripts/runTest.sh`

### Endpoint Requests example

- A: curl -s "localhost:8088/endpointa?cityname=berlin&datestring=2021-12-14" | jq .
- B: curl -s "localhost:8088/endpointb?cityname=athens&month=10" | jq .
- C: curl -s "localhost:8088/endpointc?cityname=berlin&datestring=2021-10-13" | jq .
- D: curl -s "localhost:8088/endpointd?cityname=athens&year=2015" | jq .

## Necessary improvements

- Project structure e.g. run able just with `phyton command`
- Add a proxy like Nginx to:
  - Secure connection with certificates
  - Load balancing with e.g. multiple backends
- Add logging, atm errors will be printed as "results"
- Improve Fail save for imports
  - async import e.g. buffer files (if size allow) and process  
  - broken csv (Proces by line a.t.m a failed line brake the whole import)
  - duplicate uploads (e.g. constrain by city and datetime)
  - plausibility checks like temperatures above a threshold value and so on
- Improve Request args a.t.m. there is no check for type and the value itself
- Adjust flask to productive it is atm set in Development mode with Debug and so on
- Buffer sub values / Query's to improve performance when the data reach big amounts
- Think about a NOSQL solution for raw data handling
- Config via file hold in separate repository which might be necessary if the application reach a bigger complexity and there might be multiple installations with different config needs
- Add Frontend
- Add e.g. Swagger as endpoint description