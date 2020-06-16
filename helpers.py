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


def geoCode(CountyState):
    geolocator = Nominatim(user_agent="driver.py", timeout=100)
    myLocation = geolocator.geocode(CountyState) # county+state full name is suffcient 
    return myLocation.latitude, myLocation.longitude #returns coordinates


def createMap():
    worldMap = folium.Map(
        location=[39.0119, 98.4842], #kansas coordinates haha
        zoom_start=1000,
        tiles='cartoDB dark_matter'
        )
    return worldMap

def fillCountryMap(regions, map):
    for state in regions:
        r = getState(state)
        fillStateMap(r, state, map)
    #return void


def getState(state):
    ####### dates = dates
    state = state.lower() #confirm state is lower case
    url = "https://corona.lmao.ninja/v2/historical/usacounties/{}?yesterday&strict".format(state) #state name
    r = requests.get(url)
    r = r.json()
    
    return r 

def fillStateMap(r, state, map): #1. I might be able to break this up
    countyDates = []
    countyCases = []
    if type(r)!=list:
        print(state, "had no available information")
        return 0
    for i in range(len(r)):
        countyDict = r[i]
        countyName = countyDict['county']
        countyDatesCases = countyDict['timeline']['cases']
        
        for date, case in countyDatesCases.items():
            countyDates.append(date)
            countyCases.append(case)
            
        altChart = createCaseChart(countyDates, countyCases)
        altChart = jsonChart(altChart)
        CountyState = countyName + " " + state
        addChartMarker(altChart, CountyState, map)

        countyDates.clear()
        countyCases.clear()
    #return void


def createCaseChart(x, y):
    #place data into df
    source = pd.DataFrame
    ({
        'Dates' : x,
        'Cases' : y
    })
    #Create chart
    chart = altair.Chart(source).mark_line().encode(
    x = 'Dates',
    y = 'Cases'
    )
    return chart


def jsonChart(chart):
    altair.renderers.enable('altair_viewer')
    myChart = chart
    myChart.show() # cant even show this chart, b/c can't convert to dict?? My assumption is some are empty charts
    print(type(myChart))
    chartJson = myChart.to_json()
    chartJsonLoad = json.loads(chartJson)
    return chartJsonLoad


def addChartMarker(chartJson, CountyState, map, opacity=1.0):# 1. Any other parameters? 2. May want to break this up
    lati, longi = geoCode(CountyState)
    newChart = folium.VegaLite(chartJson, width=600, height=400) 
    newPopup = folium.Popup(max_width=600)
    newChart.add_to(newPopup)
    newMarker = folium.Marker(
        location=[lati, longi],
        opacity = opacity,
        popup=newPopup,
        tooltip=CountyState
    )
    newMarker.add_to(map)
    return True # maybe void or something else


def runMap(mapFileName):
    map = createMap()
    fillCountryMap(FiftyStates, map)
    htmlSave = mapFileName + '.html'
    map.save(htmlSave)
    return htmlSave


FiftyStates = ['alabama','alaska','arizona','arkansas','california','Colorado','Connecticut','Delaware','Florida', 'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts', 'Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina', 'North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota', 'Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']



#def if __name__ == "__main__":
#    pass():

def main():
    mapname = 'MainMapUSA'
    mapHTML = runMap(mapname) # creates html file

if __name__ == "__main__":
    main()


"ERROR LOG"
"1. line61 in fillstatememap, countyDict = r[i], KeyError = 0" "FIXED BY LOWER CASING INPUT" 
"2.chartJson = chart.to_json(), missing positional argument self"
"Can't convert chart to dict, cuz no self"

"TODO"
"1. Catch errors from API" "Completed"
"2. Add Heatmap markers"