# -*- coding: utf-8 -*-
"""
PIC16B 23F Final Project by Joshua Moore and Madison Newberry
"""

import plotly.io as pio
pio.renderers.default="iframe"
import pandas as pd
import sqlite3
from plotly import express as px


def query_schools_database(state):
    """
    query_schools_database uses SQL to read through a database containing relevant school district location.
​    the state name must be the 2 letter code for the state.
    :state: the name of the state to be investigated
    """
    
    cmd = \
    f"""
    SELECT S.state, S.name, S.lat, S.lon
    FROM schools S
    WHERE S.state = "{state}"
    """
    
    return pd.read_sql_query(cmd, conn=None)

def generate_state_districts_db(state):
    """
    generates a db to be read through the query_schools_database and create a df for a specific state.
​
    :state: the name of the state to be investigated
    """
    
    conn = sqlite3.connect("schools.db") # this creates a database called schools.db.
    df_iter = pd.read_csv("All_US_Schools.csv", chunksize = 1000) # reads in our dataframe in digestible chunks of 1000 rows at a time
    if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools';").fetchone(): 
        df_iter = pd.read_csv("All_US_Schools.csv", chunksize=1000)
        for df_chunk in df_iter:
            df_chunk.to_sql("schools", conn, if_exists="append", index=False)
    df = query_schools_database(state)