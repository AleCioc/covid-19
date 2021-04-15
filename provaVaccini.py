import streamlit as st
import pandas as pd
import geojson
import os
import pydeck as pdk
import plotly.express as px
import geopandas as gpd
dati = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv"

df = pd.read_csv(dati, index_col=0)


with open(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"), encoding="utf-8") as f:
      gj = geojson.load(f)

df = df.replace("Valle d'Aosta / Vallée d'Aoste", "Valle d'Aosta/Vallée d'Aoste")

df.loc["TAA"] = df.loc['PAT']+df.loc['PAB']
df.loc["TAA","percentuale_somministrazione"]/=2
df = df.replace("Provincia Autonoma TrentoProvincia Autonoma Bolzano / Bozen", "Trentino-Alto Adige/Südtirol")


fig = px.choropleth_mapbox(df, geojson=gj, color="dosi_somministrate",
                                   locations=df.nome_area, featureidkey="properties.reg_name",
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map", zoom=4.35,
                                   color_continuous_scale="Viridis",
                                   opacity=0.7)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig, use_container_width=True)


fig = px.choropleth_mapbox(df, geojson=gj, color="percentuale_somministrazione",
                                   locations=df.nome_area, featureidkey="properties.reg_name",
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map", zoom=4.35,
                                   color_continuous_scale="Viridis",
                                   opacity=0.7)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig, use_container_width=True)



# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom, TOKEN):
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer("GeoJsonLayer",
            data,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation="0.03 * dosi_somministrate ",
            get_fill_color="[255, 255 - 13 * ( percentuale_somministrazione - 80 ) , 0 ]",
            get_line_color=[255, 255, 255],
            pickable = True,
            tooltip=True,
            auto_highlight = True
            ),
        ],
        api_keys={"mapbox": TOKEN},
        map_provider="mapbox",
        tooltip= {
   "html": "<b>Regione:</b>{reg_name}<br><b>Dosi Somministrate:</b>{dosi_somministrate}<br><b>Percentuale somministrazione:</b>{percentuale_somministrazione}%",
   "style": {
        "backgroundColor": "#231f20",
        "color": "white",
        "z-index": 2
   }
}
    )
    deck.to_html("EHYA.html")
    print("SAVED HTML")
    st.pydeck_chart(deck)


#Secondo

# view (location, zoom level, etc.)

TOKEN = "pk.eyJ1IjoiZnJhbmNlc2NvZGVhZ2xpbyIsImEiOiJja244enI0YzcxMno2MnBwOW94MXFwb2toIn0.ogZwFj2_0mfGMdwwvdkHRQ"

dati = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv"

geodf = gpd.read_file(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"), encoding="utf-8")

a = pd.merge(geodf, df, left_on="reg_name", right_on="nome_area")
print(a)

"""
for i in range(20):
    geodf.iloc[i]["dosi_somministrate"] = int(df.loc[ df["nome_area"] == geodf.iloc[i]["reg_name"] ]["dosi_somministrate"].item())
    geodf.iloc[i]["percentuale_somministrazione"] = float(
        df.loc[df["nome_area"] == geodf.iloc[i]["reg_name"]]["percentuale_somministrazione"].item())

    print(geodf.iloc[i]["dosi_somministrate"])
"""
map(a, 41.9027835, 12.4963655, 5, TOKEN)