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

filename = './CO_precincts.geojson'

with open("./CO_precincts.geojson") as geofile:
    precincts_gdf = json.load(geofile)


i=1
for feature in precincts_gdf["features"]:
    feature ['id'] = int(i)
    i += 1

##file=open(filename)
#precincts_gdf = gpd.read_file(file)
##print(type(precincts_gdf))
#print(precincts_gdf.head(1))

##precincts_gdf = gpd.read_file('CO_precincts/co_precincts.shp')
#print(precincts_gdf['geometry'].head(1))
#print(precincts_gdf['features'].head(1))

#precincts_gdf.crs = "epsg:3857"
#precincts_gdf.crs = "epsg:4326"



#create df that contains counties and lat/long for them
#df_precincts = precincts_gdf[['LABEL', 'CENT_LAT', 'CENT_LONG']]

# create empty df to initialize map
df = pd.DataFrame()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map(df, precincts_gdf):
    
    fig = go.Figure(go.Scattermapbox())
        


    #fig = go.Figure(go.scattermapbox(lat=lat, lon=lon))
    fig.update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom": 5,
            "center" :  go.layout.mapbox.Center(lat= 38.9, lon=-106.06),
            "layers":[
                {
                    "source": precincts_gdf,
                    "locations" : precincts_gdf['features']['id'],
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

### the Decorator that updates the output when a file is dragged onto the web page
### (also from https://dash.plotly.com/dash-core-components/upload)



#figure = plot_map(df, counties_gdf)
app.layout = html.Div([
    dcc.Graph(id='map',
              figure=plot_map(df,precincts_gdf)),

    #html.Div(id='output-data-upload'),
  ]
 )

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',port=port)
    app.run_server(debug=True, host="0.0.0.0", port=8050, use_reloader=True)
    

