import os
import json
#from cs50 import SQL ... do i need databases?
from flask import Flask, flash, jsonify, redirect, render_template, request, session
#from session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import requests
import folium
import geopy
from geopy.geocoders import Nominatim # to query coordinates given address
import bokeh
from bokeh.plotting import figure, output_file, show
import pip._vendor.requests as requests
from functools import wraps #check if ever needed
import urllib.parse # check if this is ever needed
from bokeh.embed import file_html
from bokeh.resources import CDN
import xml.dom.minidom
import pandas as pd
import vincent
import numpy as np
import os
import altair
from altair import Chart, X, Y, Axis, SortField



# Configure application
app= Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def homepage():
    
    return render_template('MainMapUSA.html')
