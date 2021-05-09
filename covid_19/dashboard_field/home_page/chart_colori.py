from functools import lru_cache
import requests
import time
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import pandas as pd
import geojson
import os
import plotly.express as px


class ChartColori(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Plotly", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo
        self.gj = self.get_geojson()

    def show(self):
        self.show_heading()

        with st.spinner("Sto controllando se ci sono nuovi aggiornamenti su GitHub"):
            df = self.read_data_from_git()

        with st.spinner("Sto creando la mappa. Può richiedere qualche secondo"):
                map1 = self.get_chart(df)

        st.plotly_chart(map1, use_container_width=True)


    def read_data_from_git(self):
        df = pd.read_csv(self.datalink)
        df = df.loc[df.data == max(df.data)].reset_index()

        df = df.replace({"Friuli Venezia Giulia": "Friuli-Venezia Giulia",
                         "Provincia autonoma Bolzano": "Trentino-Alto Adige/Südtirol",
                         "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste"})
        return df

    @st.cache(allow_output_mutation=True)
    def get_geojson(self):
        with open(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"),
                  encoding="utf-8") as f:
            gj = geojson.load(f)
        return gj


    @st.cache(allow_output_mutation=True, show_spinner=False)
    def get_chart(self, df):
        fig = px.choropleth_mapbox(df,
                                   geojson=self.gj, color="colore",
                                   locations=df.denominazione_regione, featureidkey="properties.reg_name",
                                   color_discrete_map={'rosso': 'red', 'giallo': 'Yellow', 'arancione': 'orange',
                                                       "bianco": "white"},
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map",
                                   zoom=4.35,
                                   opacity=0.7)

        fig.update_layout(margin={"r": 0, "t": 25, "l": 0, "b": 0})
        fig.update_layout(coloraxis_showscale=False)
        return fig

