import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

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

    # Create a dictionary with date and associated precpitation measurement
    all_prcp = []
    for date, prcp in prcp_results:
         prcp_dict = {}
         prcp_dict["date"] = date
         prcp_dict["prcp"] = prcp
         all_prcp.append(prcp_dict)

    #all_prcp = list(np.ravel(prcp_results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    # Return a JSON list of stations from the dataset.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    name_results = session.query(Station.station).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_station_names = list(np.ravel(name_results))

    return jsonify(all_station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperatures
    most_active_station = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')
    

    #temp_results = session.query(Measurement.tobs).all()

    session.close()

    most_active_list = []
    for station, date, prcp in most_active_station:
         most_active_dict = {}
         most_active_dict["station"] = station
         most_active_dict["date"] = date
         most_active_dict["prcp"] = prcp
         most_active_list.append(most_active_dict)
    
    
    return jsonify(most_active_list)

    

@app.route("/api/v1.0/temp/<start>")
def temp_start(start):

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query 

    after_start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    list = []
    for row in after_start_date:
        list.append([x for x in row])

    return jsonify(list)

@app.route("/api/v1.0/temp/<start>/<end>")
def temp_start_to_end(start, end):

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    between_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    list = []
    for row in between_start_end:
        list.append([x for x in row])

    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)
