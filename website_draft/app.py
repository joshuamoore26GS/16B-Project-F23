from flask import Flask, render_template, request
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import plotly.express as px

app = Flask(__name__)

# Initialize database connection
conn = sqlite3.connect("schools.db", check_same_thread=False)
df_iter = pd.read_csv("schools.csv", chunksize=1000)
for df_chunk in df_iter:
    df_chunk.to_sql("schools", conn, if_exists="append", index=False)

def geocode_address(address, geolocator):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def process_data(df, geolocator):
    district_lats_lons = []

    for add in df.index:
        district_lats_lons.append(df['MSTREET1'][add])

    for index, row in df.iterrows():
        address = row['MSTREET1']
        city = row['city']
        zip_code = row['MZIP']
        formatted_entry = f"{address}, {city}, {zip_code}"
        district_lats_lons.append(formatted_entry)

    district_lats_lons_2 = []
    failed_addresses = []

    for add in district_lats_lons:
        try:
            latitude, longitude = geocode_address(add, geolocator)
            if latitude is not None and longitude is not None:
                district_lats_lons_2.append([latitude, longitude])
            else:
                failed_addresses.append(add)
        except Exception as e:
            print(f"Error geocoding address {add}: {e}")
            failed_addresses.append(add)

    df2 = pd.DataFrame(district_lats_lons_2, columns=['latitude', 'longitude'])

    extracted_addresses = []
    for add in failed_addresses:
        parts = add.split(', ')
        street_address = parts[0]
        extracted_addresses.append(street_address)

    df = df[~df['MSTREET1'].isin(extracted_addresses)]
    df.reset_index(drop=True, inplace=True)

    df.loc[:, 'latitude'] = df2['latitude']
    df.loc[:, 'longitude'] = df2['longitude']

    return df

def query_schools_database(state):
    cmd = f"""
    SELECT S.statename, S.lea_name, S.mstreet1, S.mzip, S.mcity as city
    FROM schools S
    WHERE S.statename = "{state}"
    """
    df = pd.read_sql_query(cmd, conn)
    return process_data(df, Nominatim(user_agent="example app"))

@app.route('/')
def index():
    return render_template('index.html', PageTitle="CRT Data")

@app.route('/process', methods=['POST'])
def process():
    selected_state = request.form['state']
    schools_data = query_schools_database(selected_state)
    print(schools_data)
    return render_template('result.html', schools_data=schools_data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
