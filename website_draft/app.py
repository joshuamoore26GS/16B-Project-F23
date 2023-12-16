from flask import Flask, render_template, request, session
import pandas as pd
import sqlite3
import plotly.express as px


app = Flask(__name__) #creates Flask app
app.secret_key = "PIC16B" #sets secret key

# Initialize database connection
conn = sqlite3.connect("schools.db", check_same_thread=False)
# this prevents duplicate information from being added to the database, so if you run the same page multiple times you only get 1 set of information
if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools';").fetchone(): 
    df_iter = pd.read_csv("All_US_Schools.csv", chunksize=1000)
    for df_chunk in df_iter:
        df_chunk.to_sql("schools", conn, if_exists="append", index=False)
    
def state_crt_condition(state):
    """
    retrieve the status of CRT in a given state

    :state: the name of the state to be investigated
    """
    state = state.lower() # removes any casing issues
    state_crt = { # contains all the state information
        "alabama": "No CRT",
        "alaska": "CRT",
        "arizona": "CRT",
        "arkansas": "No CRT",
        "california": "CRT",
        "colorado": "CRT",
        "connecticut": "CRT",
        "delaware": "CRT",
        "florida": "No CRT",
        "georgia": "No CRT",
        "hawaii": "CRT",
        "idaho": "No CRT",
        "illinois": "CRT",
        "indiana": "CRT",
        "iowa": "No CRT",
        "kansas": "CRT",
        "kentucky": "No CRT",
        "louisiana": "CRT",
        "maine": "CRT",
        "maryland": "CRT",
        "massachusetts": "CRT",
        "michigan": "CRT",
        "minnesota": "CRT",
        "mississippi": "No CRT",
        "missouri": "CRT",
        "montana": "No CRT",
        "nebraska": "CRT",
        "nevada": "CRT",
        "new hampshire": "No CRT",
        "new jersey": "CRT",
        "new mexico": "CRT",
        "new york": "CRT",
        "north carolina": "CRT",
        "north dakota": "No CRT",
        "ohio": "CRT",
        "oklahoma": "No CRT",
        "oregon": "CRT",
        "pennsylvania": "CRT",
        "rhode island": "CRT",
        "south carolina": "No CRT",
        "south dakota": "No CRT",
        "tennessee": "No CRT",
        "texas": "No CRT",
        "utah": "No CRT",
        "vermont": "CRT",
        "virginia": "No CRT",
        "washington": "CRT",
        "west virginia": "CRT",
        "wisconsin": "CRT",
        "wyoming": "CRT",
    }
    return state_crt.get(state)
    
def state_code_conversion(state):
    """
    convert the state full name into a 2 letter code

    :state: the name of the state to be investigated
    """
    state = state.lower() # removes any casing issues
    state_codon = { # contains all the state information
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
    session["state_name"] = state_name
    selected_state = state_code_conversion(selected_state)
    session["selected_state"] = selected_state
    state_crt = state_crt_condition(state_name)
    session["state_crt"] = state_crt
    schools_data = query_schools_database(selected_state)
    prof = pd.read_csv(f"{state_name}_df.csv")
    final_df = pd.merge(schools_data, prof, on='NAME', how='left')
    conn.close()
    print(session)

    # Create Plotly figure
    fig = px.scatter_mapbox(final_df, lat='LAT', lon='LON', zoom=5, mapbox_style='carto-positron', hover_name='NAME', hover_data='Average Assessment Proficiency', color='Average Assessment Proficiency', color_continuous_midpoint=50)

    # Convert the Plotly figure to HTML
    plotly_html = fig.to_html(full_html=False)

    return render_template('result.html', schools_data=final_df, plotly_html=plotly_html, state_name=state_name, state_crt=state_crt)

@app.route('/district/<district_name>')
def district_page(district_name):
    conn = sqlite3.connect("schools.db", check_same_thread=False)
    state_name = session.get("state_name")
    selected_state = session["selected_state"]
    state_crt = state_crt_condition(state_name)
    schools_data = query_schools_database(selected_state)
    prof = pd.read_csv(f"{state_name}_df.csv")
    final_df = pd.merge(schools_data, prof, on='NAME', how='left')
    conn.close()
    district_df = final_df.loc[final_df["NAME"] == district_name] 
    
    # Create Plotly figure
    fig = px.scatter_mapbox(district_df, lat='LAT', lon='LON', zoom=5, mapbox_style='carto-positron', hover_name='NAME', hover_data='Average Assessment Proficiency', color='Average Assessment Proficiency', color_continuous_midpoint=50)

    # Convert the Plotly figure to HTML
    plotly_html = fig.to_html(full_html=False)
    
    return render_template('district_page.html', schools_data=district_df, plotly_html=plotly_html, state_name=state_name, state_crt=state_crt)

if __name__ == '__main__':
    app.run(debug=True, port=5009)