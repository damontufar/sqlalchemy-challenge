#Import Dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect = True)

#Save references to the table
Msrm = Base.classes.measurement
Stat = Base.classes.station
#Flask setup

app = Flask(__name__)

#Flask Routes

@app.route("/")
def Welcome():
    """List all available api routes."""
    return (
        """Available Routes:<br/>

        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        *You can search temperature stats from a starting date adding the date after the slash (/) with the format yyyy-mm-dd<br/>
        /api/v1.0/<start><br/>
        *You can search temperature stats between dates adding the starting date after the first slash (/) and the end after the second one with the format yyyy-mm-dd<br/>
        /api/v1.0/<start>/<end><br/>
        """
    )

@app.route("/api/v1.0/precipitation")
def daily_prcp():
    #Create session link from Python to DB
    session = Session(engine)

    """Return a list of dates and precipitation"""
    #Query dates & prcp
    results = session.query(Msrm.date, Msrm.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_data = list(np.ravel(results))

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")

def stations_names():
    #Create session link from Python to DB
    session = Session(engine)

    """Return a list of stations and names"""
    #Query station and names
    results = session.query(Stat.station, Stat.name, Stat.latitude, Stat.longitude).all()

    session.close()

    #Create a dictionary from the row data and append to a list
    station_data=[]
    for station, name, latitude, longitude in results:
        station_dict={}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_data.append(station_dict)
    

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")

def daily_temp():
    #Create session link from Python to DB
    session = Session(engine)

    """Return a list of dates and temperatures of the most active station for the last year of the data"""
    #Query station and names

    results = session.query(Msrm.date, Msrm.tobs).filter(Msrm.station == "USC00519281").filter(Msrm.date >= "2016-08-23").all()

    session.close()

    #Create a dictionary from the row data and append to a list
    daily_tobs = []
    for date, tobs in results:
        tobs_dict={}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        daily_tobs.append(tobs_dict)

    return jsonify(daily_tobs)

@app.route("/api/v1.0/<start>")

def tobs_start_date(start):
    
    #Create session link from Python to DB
    session = Session(engine)

    """Return min, max and avg temperature of for a given start date"""
    #Query temperature
    results = session.query(func.min(Msrm.tobs), func.max(Msrm.tobs), func.avg(Msrm.tobs)).filter(Msrm.date >= start).all()

    session.close()

    stats_tobs= []

    for min_tobs, avg_tobs, max_tobs in results:
        stobs_dict={}
        stobs_dict["min_tobs"] = min_tobs
        stobs_dict["avg_tobs"] = avg_tobs
        stobs_dict["max_tobs"] = max_tobs
        stats_tobs.append(stobs_dict)

    return jsonify(stats_tobs)
    
@app.route("/api/v1.0/<start>/<end>")

def tobs_between_dates(start, end):
    
    #Create session link from Python to DB
    session = Session(engine)

    """Return min, max and avg temperature of for a given start date and end date"""
    #Query temperature
    results = session.query(func.min(Msrm.tobs), func.max(Msrm.tobs), func.avg(Msrm.tobs)).filter(Msrm.date >= start). \
    filter(Msrm.date <= end).all()

    session.close()

    stats_tobs_btw= []

    for min_tobs, avg_tobs, max_tobs in results:
        stobs_dict={}
        stobs_dict["min_tobs"] = min_tobs
        stobs_dict["avg_tobs"] = avg_tobs
        stobs_dict["max_tobs"] = max_tobs
        stats_tobs_btw.append(stobs_dict)

    return jsonify(stats_tobs_btw)

if __name__ == '__main__':
    app.run(debug=True)





