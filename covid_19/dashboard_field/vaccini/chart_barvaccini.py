from functools import partial

from covid_19.dashboard_field.utils import st_functional_columns
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import altair as alt
import pandas as pd
import pydeck as pdk


class ChartBarVaccini(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Pydeck", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo

        self.traduci = {"abruzzo": "ABR", "basilicata": "BAS", "calabria": "CAL", "campania": "CAM",
               "emilia romagna": "EMR", "friuli venezia giulia": "FVG", "lazio": "LAZ",
               "liguria": "LIG", "lombardia": "LOM", "marche": "MAR", "molise": "MOL",
               "provincia autonoma Trento": "PAT", "provincia autonoma Bolzano": "PAB",
               "piemonte": "PIE", "puglia": "PUG", "sardegna": "SAR", "sicilia": "SIC",
               "toscana": "TOS", "umbria": "UMB",
               "valle d'Aosta": "VDA"
                , "veneto": "VEN"}

        #due widget, uno per scegliere la regione e uno per il mese
        wl = [
            ["selectbox", "Di quale regione?", list(self.traduci.keys())],
            ["selectbox", "Di quale mese?" , ["01", "02", "03", "04", "05"]]
        ]

        self.widget_list = [ partial(st_functional_columns, wl)]

    def show(self):
        self.show_heading()
        regione, mese = self.show_widgets()[0]
        for reg in self.traduci:
            if reg == regione:
                regione = self.traduci[regione]
                break

        with st.spinner("Sto scaricando i dati aggiornati da GitHub"):
            df = self.read_data_from_git(regione, mese)

        with st.spinner("Sto creando il barchart"):
            chart = self.get_chart(df)

        st.altair_chart(chart, use_container_width=True)

    @st.cache(show_spinner=False)
    def read_data_from_git(self, region, month):
        df = pd.read_csv(self.datalink, index_col=-1)
        in_region = df["area"] == region
        after_start_date = df["data_somministrazione"] >= "2021-"+month+"-01"
        before_end_date = df["data_somministrazione"] <= "2021-"+month+"-31"
        between_two_dates_and_in = after_start_date & before_end_date & in_region
        df = df.loc[between_two_dates_and_in]

        df = df.rename(columns={'categoria_operatori_sanitari_sociosanitari': 'Operatori (socio)sanitari',
                                'categoria_personale_non_sanitario': 'Personale non sanitario',
                                "categoria_altro": "Altro",
                                'categoria_ospiti_rsa': "Ospiti RSA",
                                'categoria_over80': "Over 80",
                                "categoria_forze_armate": "Forze armate",
                                "categoria_personale_scolastico": "Personale scolastico"})
        small = df[["data_somministrazione", "Operatori (socio)sanitari"
            , 'Personale non sanitario', 'Altro',
                    'Ospiti RSA', 'Over 80', 'Forze armate', 'Personale scolastico']]
        small = small.sort_values("data_somministrazione")
        small = small.melt(id_vars='data_somministrazione', var_name='categoria', value_name='numero_vaccini')
        return small

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df):
        return alt.Chart(df).mark_bar().encode(
            x=alt.X('sum(numero_vaccini)', title="Totale dosi somministrate"),
            y=alt.Y('data_somministrazione', title="Data di somministrazione"),
            color=alt.Color('categoria',
                            legend=alt.Legend(title="Categorie", orient="top", titleAlign="left", labelAlign="left",
                                              labelFontSize=8)),
            tooltip=["data_somministrazione", "categoria", "numero_vaccini"])
