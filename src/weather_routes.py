from __main__ import app

from ..helper.dbconnector import DbConnector

@app.route('/hello')
def hello():
    DbConnector.upload("test")
    return 'Hello, World!'