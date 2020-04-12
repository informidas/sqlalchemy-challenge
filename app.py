# import Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect existing database into new model
Base = automap_base()

# Reflect DB tables
Base.prepare(engine, reflect=True)

# Set a reference to the Station table
Station = Base.classes.station

# Set a reference to the Measurement table
measurement = Base.classes.measurement

# Generate Db Session link
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home Route
@app.route("/")
def welcome():
    """Below is a List  for our api routes."""
    return (
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature from starting date in format yyyy-mm-dd: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature for date range (start to end dates in format yyyy-mm-dd: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


# Stations route
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    precipitation_measurements = [
        Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    query_result = session.query(*precipitation_measurements).all()
    session.close()
    stations = []
    for station, name, lat, lon, el in query_result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)
    return jsonify(stations)

# Precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    precipitation_measurements = [measurement.date, measurement.prcp]
    queryresult = session.query(*precipitation_measurements).all()
    session.close()
    precipitation = []
    for date, prcp in queryresult:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

# Temperatures route
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    latest_date = session.query(measurement.date).order_by(
        measurement.date.desc()).first()[0]
    lastest_12_months = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    date_param = dt.date(lastest_12_months.year - 1,
                         lastest_12_months.month, lastest_12_months.day)
    precipitation_measurements = [measurement.date, measurement.tobs]
    query_result = session.query(
        *precipitation_measurements).filter(measurement.date >= date_param).all()
    session.close()
    alltobs = []
    for date, tobs in query_result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        alltobs.append(tobs_dict)
    return jsonify(alltobs)

# Start Date Parameter
@app.route("/api/v1.0/<startdate>")
def get_t_start(startdate):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= startdate).all()
    session.close()
    alltobs = []
    for min, avg, max in query_result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Average"] = avg
        alltobs.append(tobs_dict)
    return jsonify(alltobs)

# With Start and End Date Parameters
@app.route("/api/v1.0/<startdate>/<enddate>")
def get_t_start_stop(startdate, enddate):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= startdate).filter(
            measurement.date <= enddate).all()
    session.close()
    alltobs = []
    for min, avg, max in query_result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Average"] = avg
        alltobs.append(tobs_dict)
    return jsonify(alltobs)


if __name__ == '__main__':
    app.run(debug=True)
