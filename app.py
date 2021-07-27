# Imports
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", 
connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
        return """<html>
<h5>Hawaii Climate API</h5>

<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        year_back = dt.date(2017,8,23) - dt.timedelta(days=365)
        precip_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= year_back).\
                order_by(Measurement.date).all()
        precip_data_list = dict(precip_data)
        return jsonify(precip_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        stations = session.query(Station.station, Station.name).\
            order_by(Station.name).all()
        stations_list = dict(stations)
        return jsonify(stations_list)

# tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
        year_back = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= year_back).\
                order_by(Measurement.date).all()
        tobs_list = dict(tobs_data)
        return jsonify(tobs_list)

# STart Date Route


# End Date Route


# main
if __name__ == '__main__':
    app.run(debug=True)