import decimal
import os
from time import strptime

import psycopg2
import csv
import logging
from datetime import datetime, timedelta

insertSql = """INSERT INTO data(cityid, datetime, temperature_2m, rain,snowfall)  
            VALUES (%s, %s, %s, %s, %s) RETURNING id;"""

cityGetSql = "SELECT id FROM citynames WHERE name = %s"

cityCreateSql = "INSERT INTO citynames(name) VALUES (%s) RETURNING id;"

endpointASql = """SELECT citynames.name, to_char(data.datetime, 'YYYY-MM-DD HH:MI'), data.temperature_2m, data.rain, data.snowfall 
                FROM data 
                JOIN citynames ON citynames.id = data.cityid 
                WHERE data.datetime >= %s::date AND 
                data.datetime < %s::date AND 
                citynames.name = %s"""

endpointBSql = """SELECT to_char(daysRainPerMonth.month,'YYYY-MM'), daysRainPerMonth.count FROM  (
                    SELECT DATE_TRUNC('month',days.daysWithRain) as month, count(days.rainyday) as count FROM (
                        SELECT DATE_TRUNC('day', datetime) AS daysWithRain, 1 rainyday
                        FROM data
                        WHERE cityid = %s
                        AND rain > 0
                        GROUP BY daysWithRain
                    ) AS days
                    GROUP BY month
                ) AS daysRainPerMonth
                WHERE EXTRACT(MONTH FROM daysRainPerMonth.month) = %s 
                ORDER BY daysRainPerMonth.month"""

endpointCSql = """SELECT DATE_TRUNC('day', datetime) AS days, SUM(rain)
                FROM data
                WHERE cityid = %s AND data.datetime <= %s::date
                GROUP BY days, rain
                ORDER BY days DESC
                """

endpointDSql = """SELECT SUM(days.rain) as rainDays, SUM(days.heat) AS hotDays, SUM(days.snow) AS snowDays from (
                    SELECT DATE_TRUNC('day', datetime) AS day, 
                    CASE WHEN SUM(CASE WHEN temperature_2m > 30 THEN 1 ELSE 0 END) > 1 THEN 1 ELSE 0 END AS heat,
                    CASE WHEN SUM(CASE WHEN rain > 0 THEN 1 ELSE 0 END) > 1 THEN 1 ELSE 0 END AS rain,
                    CASE WHEN SUM(CASE WHEN snowfall > 0 THEN 1 ELSE 0 END) > 1 THEN 1 ELSE 0 END AS snow
                    FROM data
                    WHERE cityid = %s AND EXTRACT(YEAR FROM datetime) >= %s AND EXTRACT(YEAR FROM datetime) < %s
                    GROUP BY day
                    ORDER BY day
                ) AS days"""

class DbConnector:
    conn = None

    def getbycityanddate(self, cityname, datestring):
        try:
            DbConnector.connect(DbConnector)
            cur = DbConnector.conn.cursor()
            start = datetime.strptime(datestring, '%Y-%m-%d')
            end = start + timedelta(1)

            cur.execute(endpointASql, [start, end, cityname])
            resultdata = []
            for row in cur:
                resultdata.append({"name": row[0],
                                   "datetime": row[1],
                                   "temperature_2m": format(float(row[2]), '.1f'),
                                   "rain": format(float(row[3]), '.2f'),
                                   "snowfall": format(float(row[4]), '.2f')})

            result = {"success": True, "count": cur.rowcount, "data": resultdata}
        except Exception as e:
            return {"success": False, "message": e}
        finally:
            return result

    def getdayswithrainmounth(self, cityname, month):
        try:
            DbConnector.connect(DbConnector)
            cur = DbConnector.conn.cursor()
            cur.execute(cityGetSql, [cityname])
            cityid = cur.fetchone()
            if cityid == None:
                result = {"success": False, "message": "cant find a city with this name"}
            else:
                cur.execute(endpointBSql, [cityid,month])
                resultdata = []
                totalcount = 0
                for row in cur:
                    resultdata.append({"year-month": row[0],
                                       "count": row[1]})
                    totalcount += row[1]

                resultdata.append({"total for month " + month: totalcount})
                result = {"success": True, "count": cur.rowcount, "data": resultdata}

        except Exception as e:
            result = {"success": False, "message": e}
        finally:
            return result

    def getlasttimerainedindaysbynameanddate(self, cityname, datestring):
        try:
            DbConnector.connect(DbConnector)
            cur = DbConnector.conn.cursor()
            cur.execute(cityGetSql, [cityname])
            cityid = cur.fetchone()
            if cityid == None:
                result =  {"success": False, "message": "cant find a city with this name"}
            else:
                # small curser so we dont fetch all rows and can stop when the end is reached named curser are only onetime use
                cur = DbConnector.conn.cursor(name='smallCurser')
                cur.itersize = 7
                start = datetime.strptime(datestring, '%Y-%m-%d')
                cur.execute(endpointCSql, [cityid, start])
                drytimes = 0
                for row in cur:
                    if row[1] > 0:
                        #it rained
                        break
                    else:
                        drytimes += 1

                result = {"success": True, "count": 1, "data": [{"count since last rain": drytimes}]}
        except Exception as e:
            result = {"success": False, "message": e}

        finally:
            return result

    def getsnowrainheatbycityandyear(self, cityname, year):
        try:
            DbConnector.connect(DbConnector)
            cur = DbConnector.conn.cursor()
            cur.execute(cityGetSql, [cityname])
            cityid = cur.fetchone()
            if cityid == None:
                result =  {"success": False, "message": "cant find a city with this name"}
            else:
                cur.execute(endpointDSql, [cityid, str(int(year)-1), year])
                resultSet = cur.fetchone()
                result = {"success": True, "count": 3, "data": [{"heatDays": resultSet[0]},
                                                                {"rainDays": resultSet[1]},
                                                                {"snowfallDays": resultSet[2]}
                                                                ]}

        except Exception as e:
            result = {"success": False, "message": e}
        finally:
            return result

    # we don't need to close the connection here as we do it in the caller
    def getcreatecity(cityname):
        DbConnector.connect(DbConnector)
        cur = DbConnector.conn.cursor()

        try:
            cur.execute(cityGetSql, [cityname])
            cityid = cur.fetchone()
            if cityid == None:
                cur.execute(cityCreateSql, [cityname])
                cityid = cur.fetchone()[0]
                DbConnector.conn.commit()
        except:
            cityid = -1
        finally:
            return cityid

    def upload(self, file, name):
        DbConnector.connect(DbConnector)
        cur = DbConnector.conn.cursor()
        result = {"success": True}
        try:
            cityid = DbConnector.getcreatecity(name)
            if cityid < 0:
                return False

            csv_contend = [{k: v for k, v in row.items()} for row in csv.DictReader(
                file.read().decode("utf-8").splitlines(),
                skipinitialspace=True)]

            for line in csv_contend:
                cur.execute(insertSql,
                            [cityid,
                             datetime.strptime(line['time'], '%Y-%m-%dT%H:%M'),
                             line['temperature_2m'],
                             line['rain'],
                             line['snowfall']
                             ])

            self.conn.commit()

        # TODO: There can be multiple one, specific the error
        except Exception as e:
            result = {"success": False, "message": e}
        finally:
            cur.close()
            self.close(self)

        return result

    def init(self, reset):
        try:
            self.connect(self)
            cur = self.conn.cursor()
            if reset:
                cur.execute('DROP TABLE IF EXISTS data;')

            #time,temperature_2m,rain,snowfall
            cur.execute('CREATE TABLE IF NOT EXISTS data (id serial PRIMARY KEY,'
                        # we can go here with 3/1, min was −89.2 °C max 70,7 °C if we reach temp +- 100 °C but maybe we need a weather app then even more so we add one more
                        'temperature_2m NUMERIC(4, 1) NOT NULL,'
                        # rain/snow might exceed the values given by the examples so we increase it a bit
                        'rain NUMERIC(5, 2) NOT NULL,'
                        'snowfall NUMERIC(5, 2) NOT NULL,'
                        # no timezone given i assume UTC
                        'datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
                        'cityid serial NOT NULL);'
                        )
            if reset:
                cur.execute('DROP TABLE IF EXISTS citynames;')

            cur.execute('CREATE TABLE IF NOT EXISTS citynames (id serial PRIMARY KEY,'
                        # Longest city name is "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch" wich is 58 chars long but who knows, so we set a limit of 100
                        'name VARCHAR(100) NOT NULL);'
                        )

            self.conn.commit()

        finally:
            cur.close()
            self.close(self)

    def close(self):
        self.conn.close()
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=os.environ['DB_HOST'],
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USERNAME'],
                password=os.environ['DB_PASSWORD'])
