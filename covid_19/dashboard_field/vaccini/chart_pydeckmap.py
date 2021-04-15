from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import geopandas as gpd
import os
import pandas as pd
import pydeck as pdk


class ChartPydeckMap(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Pydeck", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo

    def show(self):
        self.show_heading()
        with st.spinner("Sto scaricando i dati aggiornati da GitHub"):
            df = self.read_data_from_git()

        geodf = gpd.read_file(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"),
                              encoding="utf-8")

        a = pd.merge(geodf, df, left_on="reg_name", right_on="nome_area")

        with st.spinner("Sto creando la mappa 3D"):
            deck = self.get_map(a, 40.5183188, 12.516667,  5, st.secrets["token"])
        st.pydeck_chart(deck)

    @st.cache(show_spinner=False)
    def read_data_from_git(self):
        df = pd.read_csv(self.datalink, index_col=0)
        df = df.replace("Valle d'Aosta / Vallée d'Aoste", "Valle d'Aosta/Vallée d'Aoste")

        df.loc["TAA"] = df.loc['PAT'] + df.loc['PAB']
        df.loc["TAA", "percentuale_somministrazione"] /= 2
        df = df.replace("Provincia Autonoma TrentoProvincia Autonoma Bolzano / Bozen", "Trentino-Alto Adige/Südtirol")

        return df


    @st.cache(show_spinner=False)
    def get_map(self, data, lat, lon, zoom, TOKEN):
        deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
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
            get_fill_color="[255, 255 - 10 * ( percentuale_somministrazione - 70 ) , 0 ]",
            get_line_color=[255, 255, 255],
            pickable = True,
            tooltip=True,
            auto_highlight = True
            ),
        ],
        api_keys={"mapbox": TOKEN},
        map_provider="mapbox",
        tooltip= {
        "html": "<b>Regione: </b>{reg_name}<br><b>Dosi Somministrate: </b>{dosi_somministrate}<br><b>Percentuale somministrazione: </b>{percentuale_somministrazione}%",
        "style": {
        "backgroundColor": "#231f20",
        "color": "white",
        "z-index": 2
        }
        }
        )
        return deck

