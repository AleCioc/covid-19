import datetime
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


class ChartAndamentoColori(DashboardChart):

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
            df = self.read_data_from_git(code)

        with st.spinner("Sto creando la mappa"):
            map1 = self.get_chart(df)


        st.altair_chart(map1, use_container_width=True)

    @st.cache(show_spinner=False)
    def read_data_from_git(self, code):
        df = pd.read_csv(self.datalink)

        df["end"] = df.data
        df["end"] = df["end"].apply(lambda t: datetime.datetime.fromisoformat(t) + datetime.timedelta(days=1))
        df["m"] = df["end"].apply(
            lambda t: datetime.datetime.fromisoformat(str(t)) <= datetime.datetime.now())
        return df[df["m"] == 1]


    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df):
        return alt.Chart(df).mark_bar().encode(
            x=alt.X('data:T', title="Data"),
            x2='end',
            y=alt.Y('denominazione_regione', title=""),
            color=alt.Color('colore', legend=None,
                            scale=alt.Scale(domain=["bianco", "giallo", "arancione", "rosso"],
                                            range=["white", "yellow", "orange", "red"])),
            tooltip=["data:T", "denominazione_regione", "colore"]
        ).interactive()


