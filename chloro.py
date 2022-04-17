import plotly.express as px
import json
import pandas as pd

#df = px.data.election()
#geojson = px.data.election_geojson()
with open("./CO_precincts.geojson") as geofile:
    geojson = json.load(geofile)
df = pd.read_csv("./precinct_data.csv") 

df = df[['GOV18D', 'GOV18R', 'PRECID', 'NAME']]
print(df)
df.to_csv("out.csv")

print(df.head())

print(geojson["features"][0])

print(df["PRECID"][2])
print(geojson["features"][0]["properties"])

fig = px.choropleth(df, geojson=geojson, color="GOV18D",
                    locations="NAME", featureidkey="properties.NAME",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()