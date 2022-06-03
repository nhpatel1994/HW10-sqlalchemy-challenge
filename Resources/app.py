import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/v>"
        f"/api/v1.0/temp/start<br/v>"
        f"/api/v1.0/temp/start/end<br/v>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    #Return the JSON representation of your dictionary.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of all precipitation measurements
    # Query all measurements
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_dict = []
    for date, prcp in prcp_results:
         prcp_dict = {}
         prcp_dict["date"] = date
         prcp_dict["prcp"] = prcp
         all_prcp.append(prcp_dict)

    all_prcp = list(np.ravel(prcp_results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    # Return a JSON list of stations from the dataset.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # """Return a list of all station names"""
    # # Query all stations
    name_results = session.query(Measurement.station).all()

    session.close()

    # # Convert list of tuples into normal list
    all_station_names = list(np.ravel(name_results))

    return jsonify(all_station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of all temperatures
    # Query all temperatures
    temp_results = session.query(Measurement.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temp_results))

    return jsonify(all_temps)


@app.route("/api/v1.0/temp/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return ''

    # """Return a list of passenger data including the name, age, and sex of each passenger"""
    # # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    # session.close()

    # # Create a dictionary from the row data and append to a list of all_passengers
    # all_passengers = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_passengers.append(passenger_dict)

    # return jsonify(all_passengers)

@app.route("/api/v1.0/temp/<start>/<end>")
def temp_start_to_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    return ''
    # """Return a list of passenger data including the name, age, and sex of each passenger"""
    # # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    # session.close()

    # # Create a dictionary from the row data and append to a list of all_passengers
    # all_passengers = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_passengers.append(passenger_dict)

    # return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
