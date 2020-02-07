import numpy as np
from datetime import datetime as dtt
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
    return (
        f"Welcome to the Hawaii Weather Database<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt<br/>"
        f"Enter start and/or end dates in the form YYYY-MM-DD<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a Dictionary using date as the key and prcp as the value"""
    # Query Measurement for date and precipitation
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)


@app.route("/api/v1.0/station")
def station():
    # 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a Dictionary with all the station ids and names"""
    # Query Station for station id and name
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of Temperature Observations (tobs) from a year from the last data point"""
    # Query Measurement for last date in dataset
    max_date = session.query(func.max(Measurement.date)).first()
    print(max_date)
    session.close()

    end_date = dtt.strptime(max_date[0],'%Y-%m-%d')
    start_date = end_date - dt.timedelta(days=365)

    # Query Measurement for temps from last year in dataset
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()

    # Convert list of tuples into normal list
    tobs_prev_year = list(np.ravel(results))

    return jsonify(tobs_prev_year)




@app.route('/api/v1.0/<start_date>')
def get_temps(start_date=None):
    print(f"The Start Date is:  {start_date}")
    # 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of min, average, and max temp for a given date and beyond"""
    # Query Measurement for date and precipitation for 1 year from last data point, all stations
    results = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()

    session.close()

    # Calculate min, average, and max temps and put them in a list
    temp_min = min(results)
    temp_avg = np.mean(results)
    temp_max = max(results)

    temp_list = [temp_min, temp_avg, temp_max]
    return jsonify(temp_list)


@app.route('/api/v1.0/<start_date>/<end_date>')
def get_temp_dates(start_date=None, end_date=None):
    print(f"The Start Date is:  {start_date}")
    print(f"The End Date is:  {end_date}")
    # 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of min, average, and max temp for a given date and beyond"""
    # Query Measurement for date and precipitation for 1 year from last data point, all stations
    results = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Calculate min, average, and max temps and put them in a list
    temp_min = min(results)
    temp_avg = np.mean(results)
    temp_max = max(results)

    temp_list = [temp_min, temp_avg, temp_max]
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)

