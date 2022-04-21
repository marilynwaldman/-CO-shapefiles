import plotly.express as px
import geopandas as gpd


#df = px.data.election()

geo_df = gpd.read_file('CO_precincts/co_precincts.shp').set_index("NAME")
geo_df = geo_df.to_crs("epsg:4269") #Mercator-projection
print(geo_df.head())


#    geojson["features"]
#).set_index("district")

print(type(geo_df))

fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="AG18D",
                           center={"lat": 39.7, "lon": -104.99},
                           mapbox_style="open-street-map",
                           hover_data=[ "PRECID", "AG18R"],
                           zoom=8.5)
fig.show()