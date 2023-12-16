# -*- coding: utf-8 -*-
"""
PIC16B 23F Final Project by Joshua Moore and Madison Newberry
"""

import plotly.io as pio
pio.renderers.default="iframe"
import pandas as pd
import sqlite3
from plotly import express as px

conn = sqlite3.connect("schools.db", check_same_thread=False)


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
    
    return pd.read_sql_query(cmd, conn)

def generate_state_districts_db():
    """
    generates a db to be read through the query_schools_database and create a df for a specific state.
    """
    
    conn = sqlite3.connect("schools.db") # this creates a database called schools.db.
    df_iter = pd.read_csv("All_US_Schools.csv", chunksize = 1000) # reads in our dataframe in digestible chunks of 1000 rows at a time
    if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools';").fetchone(): 
        df_iter = pd.read_csv("All_US_Schools.csv", chunksize=1000)
        for df_chunk in df_iter:
            df_chunk.to_sql("schools", conn, if_exists="append", index=False)
    conn.close() # closes the connection to the database
    
def generate_state_districts_df(state):
    """
    generates a df using the query_schools_database function, connects and closes connection to database
    :state: the name of the state to be investigated
    """
    conn = sqlite3.connect("schools.db") # this connects to the schools.db database
    df = query_schools_database(state) # this creates the df
    conn.close() # closes the connection to the database
    
    return df

def alabama_state_processing():
    """
    reads in a .csv file downloaded from https://www.alabamaachieves.org/reports-data/school-data/
    this file is renamed to "alabama_prof.csv" before this function is called
    results in a .csv file being downloaded to the computer
    """
    prof_df = pd.read_csv("alabama_prof.csv", header=None) # reads in the csv
    prof_df.columns = prof_df.iloc[4] # sets the 4th row as the column headers
    prof_df = prof_df[prof_df["Grade"] == "ALL"] # isolates only results including all student grade levels
    prof_df = prof_df[prof_df["Test Type"] == "Regular Assessment"] # only includes results for regular assessments, not specialized ones
    prof_df["ALL Category Only ***% Proficient"] = pd.to_numeric(prof_df["ALL Category Only ***% Proficient"], errors="coerce") # sets all the values to numbers in the results column
    average_scores = prof_df.groupby("System Name")["ALL Category Only ***% Proficient"].mean().reset_index() # takes the average for each district by grouping together and ungrouping
    average_scores = average_scores.rename(columns={"System Name" : "NAME", "ALL Category Only ***% Proficient": "Average Assessment Proficiency"}) # renames to a universal name for the website
    average_scores.to_csv("alabama_df.csv", index=False) # downloads the csv
    
def alaska_state_processing():
    """
    reads in a .csv file downloaded from https://education.alaska.gov/assessments/results/results2022
    this file is renamed to "AlaskaResults.csv" before this function is called
    results in a .csv file being downloaded to the computer
    """
    assess_df = pd.read_csv("AlaskaResults.csv") # reads in the csv
    assess_df.columns = assess_df.iloc[2] # sets the 2nd row as the column headers
    assess_df = assess_df[assess_df["Population"] == "All"] # isolates only results including all students, not any separated ones
    assess_df = assess_df[assess_df["Grade"] == "All"] # isolates only results including all student grade levels
    assess_df["District Name"] = assess_df["District Name"] + " School District" # adds the words "School District" to the district name
    # the following 4 lines all replace non-numeric values in the results column to allow them to be turned into numbers
    assess_df["At Target/ Advanced Percentage"] = assess_df["At Target/ Advanced Percentage"].astype(str).str.replace("*","0")
    assess_df["At Target/ Advanced Percentage"] = assess_df["At Target/ Advanced Percentage"].astype(str).str.replace("or more","")
    assess_df["At Target/ Advanced Percentage"] = assess_df["At Target/ Advanced Percentage"].astype(str).str.replace("or fewer","")
    assess_df["At Target/ Advanced Percentage"] = assess_df["At Target/ Advanced Percentage"].astype(str).str.replace("%","")
    
    assess_df["At Target/ Advanced Percentage"] = assess_df["At Target/ Advanced Percentage"].astype(float) # turns them into numbers
    assess_df["At Target/ Advanced Percentage"] = pd.to_numeric(assess_df["At Target/ Advanced Percentage"], errors="coerce") # then turns them into numerics for averaging
    average_scores = assess_df.groupby("District Name")["At Target/ Advanced Percentage"].mean().reset_index() # takes the average
    average_scores = average_scores.rename(columns={"District Name" : "NAME", "At Target/ Advanced Percentage": "Average Assessment Proficiency"}) # renames to a universal name for the website
    average_scores.to_csv("alaska_df.csv", index=False) # downloads the csv
    
    
    