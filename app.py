# Import Dependencies
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine


import json
import flask
from flask import Flask, jsonify

# Create an engine for the chinook.sqlite database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Temps API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"

    )

@app.route('/api/v1.0/precipitation')
def percipitation():
    
    conn = engine.connect()
    
    query = '''
        SELECT
            date,
            AVG(prcp) as avg_prcp
        FROM
            measurement
        WHERE
            date >= (SELECT DATE(MAX(date), '-1 year') FROM measurement)
        GROUP BY
            date
        ORDER BY
            date
'''

    prcp_df = pd.read_sql(query, conn)

    prcp_df['date'] = pd.to_datetime(prcp_df['date'])

    prcp_df.sort_values('date')

    
    prcp_json = prcp_df.to_json(orient = 'records', date_format = 'iso')
        
    conn.close()
    
    return prcp_json


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route('/api/v1.0/stations')
def station():
    
    conn = engine.connect()
    
    query = '''
        SELECT
            s.station AS station_code,
            s.name AS station_name
        FROM
            measurement m
        INNER JOIN station s
        ON m.station = s.station
        GROUP BY
            s.station,
            s.name
    '''

    active_stations_df = pd.read_sql(query, conn)
    
    active_stations_json = active_stations_df.to_json(orient = 'records')
    
    conn.close()
    
    return active_stations_json
    
if __name__ == '__main__':
    app.run(debug=True)