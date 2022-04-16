# from here:  https://github.com/mggg-states/CO-shapefiles
# here : https://community.plotly.com/t/plot-a-shapefile-shp-in-a-choropleth-chart/27850
import geopandas as gpd
import json
import pandas

#fp = "CO_precincts/co_precincts.shp"
#data = gpd.read_file(fp)

#geodf = gpd.read_file('CO_precincts/co_precincts.shp')
#geodf = geodf.to_crs("epsg:3395") #Mercator-projection

#geodf.to_file("./CO_precincts.geojson", driver = "GeoJSON")
with open("./CO_precincts.geojson") as geofile:
    j_file = json.load(geofile)

print(j_file.keys())

i=1
for feature in j_file["features"]:
    feature ['id'] = str(i).zfill(2)
    i += 1

print(type(j_file['features'][0]))
print(j_file['features'][0])
print(j_file['features'][0].keys())    





#print(geodf)
##print(type(data))
#print(data.columns)
#print(data.head())
#print(data[['NAME','COUNTYFP', 'CD116FP']])
#df = data.sort_values(by=['NAME'])
#print(df)
#