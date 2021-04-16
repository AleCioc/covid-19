from functools import partial

import requests

from covid_19.dashboard_field.utils import st_functional_columns
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import altair as alt
import pandas as pd


class ChartTempForm(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Pydeck", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo


    def show(self):
        self.show_heading()

        with st.spinner("Sto scaricando i dati aggiornati da GitHub"):
            r = requests.head(self.datalink)
            code = r.headers['Content-Length']
            df = self.read_data_from_git(code)

        with st.spinner("Sto creando il barchart"):
            chart = self.get_chart(df)

        st.altair_chart(chart, use_container_width=True)
        #b.info("Per qualche strano motivo use_container_width=True non funziona per questo grafico.")

    @st.cache(show_spinner=False)
    def read_data_from_git(self, code):
        df = pd.read_csv(self.datalink, index_col=-1)

        df_g = df[['data_somministrazione', 'fornitore',
                   'sesso_maschile', 'sesso_femminile']].groupby(["data_somministrazione", "fornitore"],
                                                                 as_index=False).sum()
        df_g["totali"] = df_g.sesso_maschile + df_g.sesso_femminile

        df1 = df[['data_somministrazione',
                  'sesso_maschile', 'sesso_femminile']].groupby(["data_somministrazione"], as_index=False).sum()
        df1["totali"] = df1.sesso_maschile + df1.sesso_femminile
        df1["fornitore"] = "Totali"

        return df1.append(df_g)

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df):
        return alt.Chart(df).mark_line().encode(
            x=alt.X('data_somministrazione:T', title="Data di somministrazione"),
            y=alt.Y('totali', title= "Numero di vaccini somministrati"),
            color=alt.Color('fornitore', title="Fornitore", legend=alt.Legend(orient="top"), sort=["Totali"]),
            tooltip=["data_somministrazione:T", "fornitore", "totali"]
)
