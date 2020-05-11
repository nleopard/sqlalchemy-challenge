#import dependecies
import datetime as dt
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import scipy.stats as sts
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Set up Database
database_path = "Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#import Flask
from flask import Flask, jsonify

#Create an app, being sure to pass __name__
app = Flask(__name__)


#Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to the Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )


#Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prec_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date
                   >= '2016-08-23').group_by(Measurement.date).all()
    return jsonify(prec_results)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    stations_results = session.query(Station.station, Station.name).all()
    return jsonify(stations_results)


#Query the dates and temperature observations of the most active station for the last year of data
#Return a JSON list of temperature observations (TOBS) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >=                                                                                         '2016-08-23').all()
    return jsonify(tobs_results)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
@app.route("/api/v1.0/<date>")
def start(date):
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(start_date)


#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    start_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                      func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(start_end_temp)


if __name__ == "__main__":
    app.run(debug=True)