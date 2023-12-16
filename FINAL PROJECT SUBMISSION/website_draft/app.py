from myProject import *
from flask import Flask, render_template, request, session
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
pio.renderers.default="iframe"


app = Flask(__name__) #creates Flask app
app.secret_key = "PIC16B" #sets secret key

myProjectDataAnalysisFunctions.generate_state_districts_db() # generates the database

@app.route('/')
def index(): # renders the initial page
    return render_template('index.html', PageTitle="School Data")

@app.route('/process', methods=['POST'])
def process(): # renders the page based on what state is chosen on the first page
    selected_state = request.form['state'] # retrieves the chosen state
    state_name = selected_state # sets a variable equal to that state
    session["state_name"] = state_name # adds it to the session
    selected_state = myProjectFlaskFunctions.state_code_conversion(selected_state) # converts the state name to its 2 letter codon
    session["selected_state"] = selected_state # adds the codon to the session
    state_crt = myProjectFlaskFunctions.state_crt_condition(state_name) # retrieves the CRT status for the state
    session["state_crt"] = state_crt # adds the CRT status to the session
    schools_data = myProjectDataAnalysisFunctions.generate_state_districts_df(selected_state) # creates a dataframe for the given state from the database
    prof = pd.read_csv(f"{state_name}_df.csv") # reads in the already-formatted state database for the given state
    final_df = pd.merge(schools_data, prof, on='NAME', how='left') # merges the dfs

    # creates a plotly figure
    fig = px.scatter_mapbox(final_df, lat='LAT', lon='LON', zoom=5, mapbox_style='carto-positron', hover_name='NAME', hover_data=['Average Assessment Proficiency'], color='Average Assessment Proficiency', color_continuous_midpoint=50)

    # converts the plotly figure to HTML for display
    plotly_html = fig.to_html(full_html=False)

    # renders the HTML template using the variables and dfs created
    return render_template('result.html', schools_data=final_df, plotly_html=plotly_html, state_name=state_name, state_crt=state_crt)

@app.route('/district/<district_name>')
def district_page(district_name): # renders a page when someone clicks on a district on the second page
    state_name = session.get("state_name") # retrieves the state name from the session
    selected_state = session.get("selected_state") # retrieves the codon from the session
    state_crt = session.get("state_crt") # retrieves the CRT status
    schools_data = myProjectDataAnalysisFunctions.query_schools_database(selected_state) # generates the same df as in the previous page
    prof = pd.read_csv(f"{state_name}_df.csv") # generates the same df as the previous page
    final_df = pd.merge(schools_data, prof, on='NAME', how='left') # merges them as in the previous page
    district_df = final_df.loc[final_df["NAME"] == district_name]  # extracts just the row from the district chosen
    
    # creates a plotly figure
    fig = px.scatter_mapbox(district_df, lat='LAT', lon='LON', zoom=5, mapbox_style='carto-positron', hover_name='NAME', hover_data=["Average Assessment Proficiency"], color='Average Assessment Proficiency', color_continuous_midpoint=50)

    # convert the plotly figure to HTML for display
    plotly_html = fig.to_html(full_html=False)
    
    # renders the HTML template using the variables and dfs created
    return render_template('district_page.html', schools_data=district_df, plotly_html=plotly_html, state_name=state_name, state_crt=state_crt)

if __name__ == '__main__':
    app.run(port=5000)
