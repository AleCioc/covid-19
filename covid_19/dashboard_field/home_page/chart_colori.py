from functools import partial

import requests

from covid_19.dashboard_field.utils import st_functional_columns
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import altair as alt
import pandas as pd
import geojson
import os
import plotly.express as px


class ChartColori(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Plotly", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo

    def show(self):
        self.show_heading()

        with st.spinner("Sto scaricando i dati aggiornati da GitHub"):
            r = requests.head(self.datalink)
            code = r.headers['Content-Length']
            #print(code)
            df, gj = self.read_data_from_git(code)

        with st.spinner("Sto creando la mappa"):
            map1 = self.get_chart(df, gj)


        st.plotly_chart(map1, use_container_width=True)

    @st.cache(show_spinner=False)
    def read_data_from_git(self, code):

        df = pd.read_csv(self.datalink)

        df = df.loc[df.data == max(df.data)].reset_index()

        with open(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"),
                  encoding="utf-8") as f:
            gj = geojson.load(f)

        df = df.replace({"Friuli Venezia Giulia": "Friuli-Venezia Giulia",
                         "Provincia autonoma Bolzano": "Trentino-Alto Adige/Südtirol",
                         "Valle d'Aosta": "Valle d'Aosta/Vallée d'Aoste"})
        return df, gj

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df, gj):
        fig = px.choropleth_mapbox(df,
                                   geojson=gj, color="colore",
                                   locations=df.denominazione_regione, featureidkey="properties.reg_name",
                                   color_discrete_map={'rosso': 'red', 'giallo': 'Yellow', 'arancione': 'orange',
                                                       "bianco": "white"},
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map", zoom=4.35,
                                   # color_continuous_scale="Viridis",
                                   opacity=0.7)
        fig.update_layout(margin={"r": 0, "t": 25, "l": 0, "b": 0})
        fig.update_layout(coloraxis_showscale=False)
        return fig

