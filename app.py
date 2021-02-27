from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from datetime import datetime, date, time
from sqlalchemy import distinct

engine=create_engine('sqlite:///Resources/hawaii.sqlite')
session=Session(engine)
Base=automap_base()
Base.prepare(engine, reflect=True)
measure=Base.classes.measurement
station=Base.classes.station
app=Flask(__name__)

@app.route('/')
def home():
	return(
	f'<h2>Available Routes:<br/>'
	f'/api/v1.0/precipitation<br/>'
	f'/api/v1.0/stations<br/>'
	f'/api/v1.0/tobs<br/>'
	f'/api/v1.0/<start><br/>'
	f'/api/v1.0/<start>/<end>')

@app.route('/api/v1.0/precipitation')
def prcp():
	p_query=session.query(measure.date, measure.prcp)\
		.filter(measure.date>='2016-08-23')\
		.filter(measure.date<='2017-08-23').all()
	results=[]
	for date, prcp in p_query:
		precipitation={}
		precipitation['date']=date
		precipitation['prcp']=prcp
		results.append(precipitation)
	session.close()
	return jsonify(results)

@app.route('/api/v1.0/stations')
def stations():
	s_query=session.query(station.station).all()
	all_stations=list(np.ravel(s_query))
	return jsonify(all_stations)
	session.close()

@app.route('/api/v1.0/tobs')
def temp():
	t_query=session.query(station.station, measure.date, measure.tobs)\
	.filter(measure.date >= "2016-08-24")\
   	.filter(measure.date <= "2017-08-23")\
   	.filter(station.station == "USC00519281").all()
	temp_data=list(np.ravel(t_query))
	return jsonify(temp_data)
	session.close()

@app.route('/api/v1.0/<start>')
def start(start):
	start_date = datetime.strptime(start,"%Y-%m-%d").date()
	temp=session.query(func.min(measure.tobs),func.max(measure.tobs), func.avg(measure.tobs))\
		.filter(measure.date>=start_date).all()
	results_temp=list(np.ravel(temp))
	min_temp= results_temp[0]
	avg_temp= results_temp[1]
	max_temp= results_temp[2]

	temp_data=[]
	temp_dict= [{"Start Date": start_date},\
	{"The min temperature for this date was": min_temp},\
	{"The average temperature for this date was": avg_temp},\
	{"The max temperature for this date was": max_temp}]
	temp_data.append(temp_dict)
	session.close()

	return jsonify(temp_data)
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
	start_date = datetime.strptime(start,"%Y-%d-%Y").date()
	end_date = datetime.strptime(end,"%m-%d-%Y").date()
	temp = session.query (func.min(Measurement.tobs), func.max (Measurement.tobs), func.avg (Measurement.tobs))\
    	.filter(Measurement.date >= start_date)\
    	.filter(Measurement.date <= end_date).all()
	temp_results = list(np.ravel(temp_calc))

	min_temp = temp_results[0]
	max_temp = temp_results[1]
	avg_temp = temp_results[2]

	temp_data = []
	temp_dict = [{"Start Date": start_date},{"End Date": end_date},
    	{"Minimum Temperature for this date range": min_temp},
    	{"Maximum Temperature for this date range": max_temp},
    	{"Average Temperature for this date range": avg_temp}]
	temp_data.append(temp_dict)
	return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)


