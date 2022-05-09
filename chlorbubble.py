# from https://plotly.com/python/mapbox-county-choropleth/
import dash
from dash import dcc 
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.express as px
import base64
import io
import numpy as np
from urllib.request import urlopen
import json
import plotly.graph_objects as go


# Read tx counties

# read in data
pop_df = pd.read_csv("County Pop Data.csv")
cases_df = pd.read_csv("Texas county COVID cases data clean.csv")


cities_df = pd.read_csv("uscities.csv") #need for plotting texas cities
pop_df = pop_df.drop("Unnamed: 0", axis = 1)
cases_df["7 day diff"] = cases_df.iloc[:, -1] - cases_df.iloc[:, -8]
#conda install openpyxl
fips_data = pd.read_excel("PHR_MSA_County_masterlist.xlsx", dtype={'FIPS #': str}) #need this to plot counties on map

# some counties have a negative 7 day diff so lets replace the neg with 0
def replace_neg(s):
    if s < 0:
        return 0
    else:
        return s

cases_df["7 day diff"] = cases_df["7 day diff"].map(replace_neg)

#merging population data with time series cases data
df = cases_df.merge(pop_df,how = "left", left_on = "County Name", right_on = "County").drop("County", axis = 1)
df["Cases per 100000 population"] = (df["7 day diff"] / df["Total Population"]) * 100000
bin_labels_8 = ["very low", "low","low/medium", "medium", "medium/high","high", "very high", "extreme"]
df["Bin Cases per 100000 population"] = pd.qcut(df["Cases per 100000 population"], q=8, \
                                                duplicates = "drop", labels=bin_labels_8)
print(df.head())

fips_df = fips_data[["County Name", "FIPS #"]]


def add_48(s):
    return "48" + str(s)

fips_df["FIPS #"] = fips_df["FIPS #"].map(add_48)
print(fips_df.head())

df2 = df.merge(fips_df,how = "left", left_on = "County Name", right_on = "County Name")
print(df2.head())

# dropping totals rows 
df2 = df2.drop([254, 255])
df2['FIPS #'] = df2['FIPS #'].astype(str)

df3 = df2[["County Name", "FIPS #", "Cases per 100000 population"]]
df3.to_csv("geo_cases_plotly.csv")

max_cases = df3["Cases per 100000 population"].max()

# for plotting major texas cities
mask = cities_df["state_id"] == "TX"
texas_cities = cities_df[mask]

mask2 = texas_cities["population"] > 200000
big_texas_cities = texas_cities[mask2]

cities_for_map = big_texas_cities[["city", "lat", "lng"]]

print(px.colors.qualitative.Dark2)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("bubble_geo_cases_plotly.csv")
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map(df, counties):
    fig = px.choropleth(df, geojson=counties, locations='FIPS #',
                           hover_name = "County",
                           scope = "usa",
                          )
    colors = ['rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)','rgb(239,243,255)']
    months = {5: 'May', 6:'June',7:'July',8:'Aug'}

    for i in range(5,9)[::-1]:
        mask = df["month"] == i
        df_month = df[mask]
        #print(df_month)
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_month['X (Lat)'],
            lat = df_month['Y (Long)'],
            text = df_month[['County','Case Count']],
            name = months[i],
            mode = 'markers',
            marker = dict(
                size = df_month['Case Count'],
                color = colors[i-6],
                line_width = 0,
                sizeref = 9,
                sizemode = "area", 
                reversescale = True
            )))

    # to show texas cities on map
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = cities_for_map['lng'],
        lat = cities_for_map['lat'],
        hoverinfo = 'text',
        text = cities_for_map['city'],
        name = "Major Cities",
        mode = 'markers',
        marker = dict(
            size = 4,
            color = 'rgb(102,102,102)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))

    fig.update_geos(fitbounds="locations")
    fig.update_layout(title_text='Total Cases per month for last 4 months', title_x=0.5)         
    
 

    return fig

        


#figure = plot_map(df, counties_gdf)
app.layout = html.Div([
    dcc.Graph(id='map',
        figure=plot_map(df,counties)),
  ]
 )

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',port=port)
    app.run_server(debug=True, host="0.0.0.0", port=8050, use_reloader=False)
    

