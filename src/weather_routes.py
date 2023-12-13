from flask import Blueprint, render_template, request, session, abort, redirect
from src.helper.dbconnector import DbConnector

routes = Blueprint('weather_routes', __name__)

@routes.route('/upload', methods = ['POST'])
def upload():
    uploaded_file = request.files['file']
    cityname = request.form.get("cityname")
    if DbConnector.upload(DbConnector, uploaded_file, cityname):
        return {'success': True}, 200
    else:
        return {'success': False, 'message': 'Error while uploading data'}, 400

# date format 2021-12-14
@routes.route('/endpointa')
def endpointa():
    cityname = request.args.get('cityname')
    datestring = request.args.get('datestring')
    result = DbConnector.getbycityanddate(DbConnector, cityname, datestring)
    if result["success"] is True:
        return result, 200
    else:
        return {"success": False, "message": "Error while get data: " + result["message"]}, 400

@routes.route('/endpointb')
def endpointb():
    cityname = request.args.get('cityname')
    month = request.args.get('month')
    result = DbConnector.getdayswithrainmounth(DbConnector, cityname, month)
    if result["success"] is True:
        return result, 200
    else:
        return {"success": False, "message": "Error while get data: " + result["message"]}, 400


@routes.route('/endpointc')
def endpointc():
    cityname = request.args.get('cityname')
    datestring = request.args.get('datestring')
    result = DbConnector.getlasttimerainedindaysbynameanddate(DbConnector, cityname, datestring)
    if result["success"] is True:
        return result, 200
    else:
        return {"success": False, "message": "Error while get data: " + result["message"]}, 400

@routes.route('/endpointd')
def endpointd():
    cityname = request.args.get('cityname')
    year = request.args.get('year')
    result = DbConnector.getsnowrainheatbycityandyear(DbConnector,  cityname, year)
    if result["success"] is True:
        return result, 200
    else:
        return {"success": False, "message": "Error while get data: " + result["message"]}, 400
