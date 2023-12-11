# WeatherdataAPI

## Task description

Weather data API
The goal of this project is to create an API that serves historical weather information and statistics. The
historical weather information for each city will be provided in a file. The file contains:
•
•
•
The timestamp of the weather information (granularity is hour).
The average temperature 2m above ground (in Celcius).
Rain and snow (mm) for that hour.
One file (CSV) for each city will be used. Please find attached two example CSV files for Berlin and
Athens.
Deliverables
The following must be part of the solution.
•
•
Scripts to import data to a Postgres database.
A service with the following endpoints:
o An endpoint to get all available weather information for a given city and date.
o An endpoint to get the number of days with rain for a given city and month.
o An endpoint to get the number of days since it last rained for a given city and date.
o An endpoint to provide the number of days it rained, the number of days it was snowed
and the number of days with extreme heat (temperature was > 30 C sometime during
the day) for a given year and city.
Please provide a .zip file or access to a private git repo containing:
•
•
•
The source code.
Instructions on how to setup, run and access the endpoints.
Anything else that you consider important.
