# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    """List of all available API routes"""

    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_to_end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >='2016-08-23').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into a dictionary
    
    precipitation = []
    for prcp_data in results:
        prcp_data_dict = {}
        prcp_data_dict["Date"] = prcp_data.date
        prcp_data_dict["Precipitation"] = prcp_data.prcp
        precipitation.append(prcp_data_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    # Create a session (link) from Python to the DB

    session = Session(engine)

    """Return a list of all station names"""

    results = session.query(Station.name).all()

    session.close()
    
    # Convert list of tuples of all stations into normal list
    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the dates and temperature observations of the most-active station for the previous year of data.

    session = Session(engine)

    """Return a list of dates and temperature observations of the most-active station for the previous year."""
    
    results = session.query((Measurement.date), (Measurement.tobs)).filter(Measurement.station=='USC00519281').order_by(Measurement.date >='2016-08-23').all()
    
    session.close()

    # Convert list of tuples of dates and temperature observations into normal list

    active_stations = list(np.ravel(results))

    return jsonify(active_stations)

@app.route("/api/v1.0/start")
def start():
    
    start_date = input(f"Enter a start date.")

    session = Session(engine)

    """Return a list of the minimum temp, average temp and maximum temp for a given start date"""

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Convert list of tuples to a dictionary

    temp_start = []

    for Tmin, Tave, Tmax in results:
        temp_start_dict = {}
        temp_start_dict["TMIN"] = Tmin
        temp_start_dict["TAVE"] = Tave
        temp_start_dict["TMAX"] = Tmax
        temp_start.append(temp_start_dict)

    return jsonify (temp_start)

@app.route("/api/v1.0/start_to_end")
def start_to_end():

    start_date = input(f"Enter start date.")
    end_date = input(f"Enter end date.")

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    temp_start_end = []

    for Tmin, Tave, Tmax in results:
        temp_start_end_dict = {}
        temp_start_end_dict["TMIN"] = Tmin
        temp_start_end_dict["TAVE"] = Tave
        temp_start_end_dict["TMAX"] = Tmax
        temp_start_end.append(temp_start_end_dict)

    return jsonify (temp_start_end)   

if __name__ == '__main__':
    app.run(debug=True)

