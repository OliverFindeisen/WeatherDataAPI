import os
import psycopg2
import logging

class DbConnector():
        conn = None

        def connect(self):
            if self.conn == None:
               self.conn = psycopg2.connect(
                    host="localhost",
                    database="weather",
                    #user=os.environ['DB_USERNAME'],
                    user="weather",
                    #user=os.environ['DB_USERNAME'],
                    password="test")

        def upload(data):
            logging.warning(data)
            DbConnector.connect(DbConnector)
            cur = DbConnector.conn.cursor()
            cur.execute('SELECT count(*) FROM books')

            cur.close()