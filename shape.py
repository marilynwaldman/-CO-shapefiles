# from here:  https://github.com/mggg-states/CO-shapefiles
# here : https://community.plotly.com/t/plot-a-shapefile-shp-in-a-choropleth-chart/27850
import geopandas as gpd
import json
import pandas

#fp = "CO_precincts/co_precincts.shp"
#data = gpd.read_file(fp)

#geodf = gpd.read_file('CO_precincts/co_precincts.shp')
#geodf = geodf.to_crs("epsg:4269") #Mercator-projection

#geodf.to_file("./CO_precincts.geojson", driver = "GeoJSON")
with open("./CO_precincts.geojson") as geofile1:
    j_file1 = json.load(geofile1)

print(j_file1.keys())

  
print(j_file1.keys())

print(j_file1['crs'])


print(type(j_file1['features'][0]))

print(j_file1['features'][0].keys())
