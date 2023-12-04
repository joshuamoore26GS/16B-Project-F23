from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import plotly.express as px


app = Flask(__name__)

<<<<<<< Updated upstream
# Initialize database connection
conn = sqlite3.connect("schools.db", check_same_thread=False)
df_iter = pd.read_csv("schools.csv", chunksize=1000)
for df_chunk in df_iter:
    df_chunk.to_sql("schools", conn, if_exists="append", index=False)

# Load the geocoded data CSV file
geocoded_df = pd.read_csv("geocoded_data.csv")

def query_schools_database(state):
    cmd = f"""
    SELECT S.statename, S.lea_name, S.mstreet1, S.mzip, S.mcity as city
    FROM schools S
    WHERE S.statename COLLATE NOCASE = "{state}"
    """

    print("SQL Query:")
    print(cmd)

    df = pd.read_sql_query(cmd, conn)
    print("Resulting DataFrame:")
    print(df)

    return df

=======
>>>>>>> Stashed changes
@app.route('/')
def index():
    return render_template('index.html', PageTitle="CRT Data")

@app.route('/process', methods=['POST'])
def process():
    selected_state = request.form['state']
    schools_data = geocoded_df

    # Create Plotly figure
    fig = px.scatter_mapbox(schools_data, lat='latitude', lon='longitude', zoom=1, mapbox_style='carto-positron', hover_name='Name')

    # Convert the Plotly figure to HTML
    plotly_html = fig.to_html(full_html=False)

    return render_template('result.html', schools_data=schools_data, plotly_html=plotly_html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
