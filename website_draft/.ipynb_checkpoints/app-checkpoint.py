from flask import Flask, render_template, request
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import plotly.express as px

app = Flask(__name__)

# Initialize  database connection
conn = sqlite3.connect("schools.db")


def query_schools_database(state):
    cmd = f"""
    SELECT S.statename, S.lea_name, S.mstreet1, S.mzip
    FROM schools S
    WHERE S.statename = "{state}"
    """
    return pd.read_sql_query(cmd, conn)


def geocode_address(address):
    geolocator = Nominatim(user_agent="example app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html', PageTitle="CRT Data")

@app.route('/process', methods=['POST'])
def process():
    selected_state = request.form['state']
    schools_data = query_schools_database(selected_state)
    return render_template('result.html', schools_data=schools_data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)


    

 



