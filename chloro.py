import plotly.express as px
import plotly.graph_objects as go
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
                    projection="mercator",
                    color_continuous_scale=px.colors.diverging.RdGy[::-1],
                    title = "CO Precienct Repubican Votes Governor 2018 ",
                    hover_data=["GOV18D", "GOV18R", 'NAME', "PRECID"]
                   )
fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(title = "Democratic Governors Race")
fig.show()