import dash
from dash import dcc 
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import base64
import io
import numpy as np

fp = "CO_precincts/co_precincts.shp"
data = gpd.read_file(fp)

#initialize county polygons
filename = './co_counties_voters.geojson'
file=open(filename)
counties_gdf = gpd.read_file(file)

 = gpd.read_file('CO_precincts/co_precincts.shp')

#create df that contains counties and lat/long for them
df_counties = counties_gdf[['LABEL', 'CENT_LAT', 'CENT_LONG']]

# create empty df to initialize map
df = pd.DataFrame()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,prevent_initial_callbacks=True)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map(df, counties_gdf):
    
    fig = go.Figure(go.Scattermapbox())
        
    if  not df.empty:
        lats, lons, labels, sizes, colors = get_map_attributes(df)

        fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = lons,
        lat = lats,
        text = labels,
        marker = {'size': sizes, 'color': colors},
        
        ))

    

    
    #fig = go.Figure(go.scattermapbox(lat=lat, lon=lon))
    fig.update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom": 5,
            "center" :  go.layout.mapbox.Center(lat= 38.9, lon=-106.06),
            "layers":[
                {
                    "source": json.loads(counties_gdf.geometry.to_json()),
                    "below":"traces",
                    "type":"line",
                    "color":"purple",
                    "line":{"width": 1.5}
                }
            ],
        },
        margin={"l":0,"r":0,"t":0,"b":0},
    ) 

    fig.update_traces(line=dict(width=3, color='black'))
    
    return fig
