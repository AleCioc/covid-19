from functools import partial

import requests

from covid_19.dashboard_field.utils import st_functional_columns
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import altair as alt
import pandas as pd


class ChartBarVax(DashboardChart):

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
        a, b = st.beta_columns((0.80, 0.20))
        with a:
            st.altair_chart(chart, use_container_width=True)
        #b.info("Per qualche strano motivo use_container_width=True non funziona per questo grafico.")

    @st.cache(show_spinner=False)
    def read_data_from_git(self, code):
        df = pd.read_csv(self.datalink, index_col=-1)
        grouped = df.groupby("fornitore", as_index=False).sum()
        grouped = grouped[["fornitore", 'categoria_operatori_sanitari_sociosanitari',
                           'categoria_personale_non_sanitario', 'categoria_ospiti_rsa',
                           'categoria_over80', 'categoria_forze_armate',
                           'categoria_personale_scolastico', 'categoria_altro', "categoria_soggetti_fragili", "categoria_60_69", "categoria_70_79"]]

        grouped = grouped.rename(columns={'categoria_operatori_sanitari_sociosanitari': '(Socio)Sanitari',
                                          'categoria_personale_non_sanitario': 'Non sanitario',
                                          "categoria_altro": "Altro",
                                          'categoria_ospiti_rsa': "Ospiti RSA",
                                          'categoria_over80': "Over 80",
                                          "categoria_forze_armate": "Forze armate",
                                          "categoria_personale_scolastico": "Scolastico",
                                          "categoria_soggetti_fragili": "Soggetti fragili",
                                          "categoria_60_69": "60-69",
                                          "categoria_70_79": "70-79"
                                          })
        grouped = grouped.melt(id_vars='fornitore', var_name='categoria', value_name='numero_vaccini')
        return grouped

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df):
        return alt.Chart(df).mark_bar().encode(
            y=alt.X('fornitore:O', title=""),
            x=alt.Y('sum(numero_vaccini):Q', title="Numero vaccini"),
            color=alt.Color('fornitore',title="", legend=alt.Legend(orient="top")),
            row=alt.Row('categoria:N', title=""),
            tooltip=["fornitore", "categoria", "numero_vaccini"],
        )
