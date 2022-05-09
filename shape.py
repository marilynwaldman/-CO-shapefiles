# from here:  https://github.com/mggg-states/CO-shapefiles
# here : https://community.plotly.com/t/plot-a-shapefile-shp-in-a-choropleth-chart/27850
import geopandas as gpd
import json
import pandas

fp = "blocks/blocks.shp"
data = gpd.read_file(fp)
data['IDX'] = data.index
print(data.head(1))

#geodf = gpd.read_file('CO_precincts/co_precincts.shp')
#geodf = geodf.to_crs("epsg:4269") #Mercator-projection

#geodf.to_file("./CO_precincts.geojson", driver = "GeoJSON")
#with open("./CO_precincts.geojson") as geofile1:
#    j_file1 = json.load(geofile1)

