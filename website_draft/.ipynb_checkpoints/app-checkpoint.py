from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import plotly.express as px

app = Flask(__name__)

# Initialize database connection
conn = sqlite3.connect("schools.db", check_same_thread=False)
# this prevents duplicate information from being added to the database, so if you run the same page multiple times you only get 1 set of information
if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools';").fetchone(): 
    df_iter = pd.read_csv("All_US_Schools.csv", chunksize=1000)
    for df_chunk in df_iter:
        df_chunk.to_sql("schools", conn, if_exists="append", index=False)

    
def state_code_conversion(state):
    """
    convert the state full name into a 2 letter code

    :state: the name of the state to be investigated
    """
    state = state.lower() # removes any casing issues
    state_codon = {
        "alabama": "AL",
        "alaska": "AK",
        "arizona": "AZ",
        "arkansas": "AR",
        "california": "CA",
        "colorado": "CO",
        "connecticut": "CT",
        "delaware": "DE",
        "florida": "FL",
        "georgia": "GA",
        "hawaii": "HI",
        "idaho": "ID",
        "illinois": "IL",
        "indiana": "IN",
        "iowa": "IA",
        "kansas": "KS",
        "kentucky": "KY",
        "louisiana": "LA",
        "maine": "ME",
        "maryland": "MD",
        "massachusetts": "MA",
        "michigan": "MI",
        "minnesota": "MN",
        "mississippi": "MS",
        "missouri": "MO",
        "montana": "MT",
        "nebraska": "NE",
        "nevada": "NV",
        "new hampshire": "NH",
        "new jersey": "NJ",
        "new mexico": "NM",
        "new york": "NY",
        "north carolina": "NC",
        "north dakota": "ND",
        "ohio": "OH",
        "oklahoma": "OK",
        "oregon": "OR",
        "pennsylvania": "PA",
        "rhode island": "RI",
        "south carolina": "SC",
        "south dakota": "SD",
        "tennessee": "TN",
        "texas": "TX",
        "utah": "UT",
        "vermont": "VT",
        "virginia": "VA",
        "washington": "WA",
        "west virginia": "WV",
        "wisconsin": "WI",
        "wyoming": "WY",
    }
    return state_codon.get(state)

def query_schools_database(state):
    """
    query_schools_database uses SQL to read through a database containing relevant school district location.

    :state: the name of the state to be investigated
    """
    
    cmd = \
    f"""
    SELECT S.state, S.name, S.lat, S.lon
    FROM schools S
    WHERE S.state = "{state}"
    """
    
    return pd.read_sql_query(cmd, conn)



@app.route('/')
def index():
    return render_template('index.html', PageTitle="School Data")

@app.route('/process', methods=['POST'])
def process():
    conn = sqlite3.connect("schools.db", check_same_thread=False)
    selected_state = request.form['state']
    state_name = selected_state
    selected_state = state_code_conversion(selected_state)
    schools_data = query_schools_database(selected_state)
    conn.close()

    # Create Plotly figure
    fig = px.scatter_mapbox(schools_data, lat='LAT', lon='LON', zoom=5, mapbox_style='carto-positron', hover_name='NAME')

    # Convert the Plotly figure to HTML
    plotly_html = fig.to_html(full_html=False)

    return render_template('result.html', schools_data=schools_data, plotly_html=plotly_html, state_name=state_name)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
