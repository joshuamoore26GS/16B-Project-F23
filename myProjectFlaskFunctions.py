# -*- coding: utf-8 -*-
"""
PIC16B 23F Final Project by Joshua Moore and Madison Newberry
"""

from flask import Flask, render_template, request, session
import pandas as pd
import sqlite3
import plotly.express as px


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