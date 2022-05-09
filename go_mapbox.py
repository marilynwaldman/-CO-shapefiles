import geopandas as gpd
import plotly.graph_objects as go
import dash
from dash import dcc 
from dash import html
import json



#df = px.data.election()

geo_df = gpd.read_file('CO_precincts/co_precincts.shp')
geo_df = geo_df.to_crs("WGS84").set_index("NAME")

#geo_df = geo_df.to_crs("epsg:WGS84") #Mercator-projection
print(geo_df.head())
print(type(geo_df.geometry))


#    geojson["features"]
#).set_index("district")

print(type(geo_df))

xxx = geo_df.geometry.to_json()
print(type(xxx))

"""
fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="AG18D",
                           center={"lat": 39.7, "lon": -104.99},
                           mapbox_style="open-street-map",
                           hover_data=[ "PRECID", "AG18R"],
                           zoom=8.5)
fig.show()
"""


fig = go.Figure(go.Choroplethmapbox(geojson=json.loads(geo_df.to_json()),
                                    #featureidkey = "properties.NAME", #Assign feature key 
                                    locations=geo_df.index, z=geo_df['AG18D'],
                                    colorscale="Viridis", marker_line_width=.5))

fig.update_layout(mapbox_style="open-street-map",
                        height = 1000,
                        autosize=True,
                        margin={"r":0,"t":0,"l":0,"b":0},
                        paper_bgcolor='#303030',
                        plot_bgcolor='#303030',
                        mapbox=dict(center=dict(lat=39.7, lon=-104.99),zoom=9),
                        )


fig.show()
