#Import Dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        /api/v1.0/<start><br/>
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

if __name__ == '__main__':
    app.run(debug=True)





