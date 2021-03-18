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

#Flask setup

app = Flask(__name__)

#Flask Routes

@app.route("/")
def Welcome():
    """List all available api routes."""
    return (
        """Available Routes:<br/>
        /api/v1.0/precipitation
        """
    )

@app.route("/api/v1.0/precipitation")
def names():
    #Create session link from Python to DB
    session = Session(engine)

    """Return a list of dates and precipitation"""
    #Query dates & prcp
    results = session.query(Msrm.dates, Msrm.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_data = list(np.ravel(results))

    return jsonify(prcp_data)

if __name__ == '__main__':
    app.run(debug=True)





