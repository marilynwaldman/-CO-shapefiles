import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import geopandas as gpd

geo_df = gpd.read_file('blocks/blocks.shp')
geo_df['IDX'] = geo_df.index
geo_df = geo_df.to_crs("epsg:4269") #Mercator-projection
print(geo_df.head())



fig = px.choropleth(geo_df, geojson=geo_df, color="COUNTYFP10",
                    locations="IDX", featureidkey="properties.IDX",
                    projection="mercator",
                    color_continuous_scale=px.colors.diverging.RdGy[::-1],
                    title = "CO Precienct Repubican Votes Governor 2018 ",
                    hover_data=["TRACTCE10", "BLOCKCE10", "GEOID10", "NAME10" ]
                   )
fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(title = "Blocks")
fig.show()