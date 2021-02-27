
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
import datetime as dt
from datetime import datetime, date, time

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
		f'<h2>SQLALCHEMY-CHALLENGE</h2>'
		f'<h3>Available Routes:<br/></h3>'
		f'<strong>Date Input Format --> YYYY-MM-DD<br/></strong>'
		f'<br/>'
		f"/api/v1.0/precipitation<br/>"
		f'/api/v1.0/stations<br/>'
		f'/api/v1.0/tobs<br/>'
		f'/api/v1.0/start_date<br/>'
		f'/api/v1.0/start_date/end_date<br/>'
	)

@app.route("/api/v1.0/precipitation")
def prcp():
	session=Session(engine)
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
	session=Session(engine)
	s_query=session.query(station.station).all()
	all_stations=list(np.ravel(s_query))
	return jsonify(all_stations)
	session.close()

@app.route('/api/v1.0/tobs')
def temp():
	session=Session(engine)
	t_query=session.query(station.station, measure.date, measure.tobs)\
	.filter(measure.date >= "2016-08-24")\
   	.filter(measure.date <= "2017-08-23")\
   	.filter(station.station == "USC00519281").all()
	temp_data=list(np.ravel(t_query))
	return jsonify(temp_data)
	session.close()

@app.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)

    temp_calc= session.query(func.min(measure.tobs), func.avg(measure.tobs), func.max(measure.tobs)).\
        filter(measure.date >= start).all()

    results_temp= list(np.ravel(temp_calc))

    min_temp= results_temp[0]
    avg_temp= results_temp[1]
    max_temp= results_temp[2]

    temp_data=[]
    temp_dict= [{"Start Date": start},
    {"The min temperature for this date was": min_temp},
    {"The avg temperature for this date was": avg_temp},
    {"The max temperature for this date was": max_temp}]
    temp_data.append(temp_dict)
    session.close()

    return jsonify(temp_data)


@app.route("/api/v1.0/temp/<start>/<end>")
def end(start,end):
    session=Session(engine)

    trip_calcs= session.query(func.min(measure.tobs), func.avg(measure.tobs), func.max(measure.tobs)).\
        filter(measure.date >= start).filter(measure.date<=end).all()

    trip_result= list(np.ravel(trip_calcs))

    min_temp_trip= trip_result[0]
    avg_temp_trip= trip_result[1]
    max_temp_trip= trip_result[2]

    trip_data=[]

    trip_dict= [{"Start Date": start},
    
    {"The min temperature for this date was": min_temp_trip},
    {"The avg temperature for this date was": avg_temp_trip},
    {"The max temperature for this date was": max_temp_trip},
    {"End Date": end}]
    trip_data.append(trip_dict)
    session.close()

    return jsonify(trip_data)

if __name__ == '__main__':
    app.run(debug=True)


