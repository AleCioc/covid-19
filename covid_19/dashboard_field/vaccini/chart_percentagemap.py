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


class ChartPercentageMap(DashboardChart):

    def __init__(self, name, title, subtitle, datalink, tipo = "Plotly", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.datalink = datalink
        self.tipo = tipo
        #due widget, uno per scegliere la regione e uno per il mese
        self.categorie = ["over80", "sanitari", "scolastici", "rsa", "70-79"]
        wl = [
            ["selectbox", "Di quale categoria?" , self.categorie]
        ]
        self.widget_list = [ partial(st_functional_columns, wl)]

    def show(self):
        self.show_heading()
        categoria = self.show_widgets()[0][0]

        with st.spinner("Sto scaricando i dati aggiornati da GitHub"):
            r = requests.head(self.datalink)
            code = r.headers['Content-Length']
            df, gj = self.read_data_from_git(categoria, code)

        with st.spinner("Sto creando le due mappe"):
            map1, map2 = self.get_chart(df, gj)

        col1, col2 = st.beta_columns(2)
        col1.plotly_chart(map1, use_container_width=True)
        col2.plotly_chart(map2, use_container_width=True)

        st.image(os.path.join(os.curdir, "ViridisContinuousContinuous.png"),
                 caption="Colorscale utilizzata, valori crescenti da sinistra verso destra")

    @st.cache(show_spinner=False)
    def read_data_from_git(self, categoria, code):

        df = pd.read_csv(self.datalink, index_col=1)
        df = df.loc[df.report == max(df.report)]
        df = df.loc[df.index == categoria]

        with open(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"),
                  encoding="utf-8") as f:
            gj = geojson.load(f)

        df = df.append(df.loc[df.regione == 'PAT'] + df.loc[df.regione == 'PAB'])
        df = df.replace("PATPAB", "TAA")

        df["percentuale1dose"] = 100 * df["prima_dose"] / df["popolazione"]
        df["percentuale2dose"] = 100 * df["seconda_dose"] / df["popolazione"]

        df = df.replace({"ABR": "Abruzzo", "BAS": "Basilicata", "CAL": "Calabria", "CAM": "Campania",
                         "EMR": "Emilia-Romagna", "FVG": "Friuli-Venezia Giulia", "LAZ": "Lazio",
                         "LIG": "Liguria", "LOM": "Lombardia", "MAR": "Marche", "MOL": "Molise",
                         "TAA": "Trentino-Alto Adige/Südtirol", "PIE": "Piemonte", "PUG": "Puglia", "SAR": "Sardegna",
                         "SIC": "Sicilia",
                         "TOS": "Toscana", "UMB": "Umbria", "VDA": "Valle d'Aosta/Vallée d'Aoste", "VEN": "Veneto"})

        return df, gj

    @st.cache(show_spinner=False, allow_output_mutation=True)
    def get_chart(self, df, gj):
        fig = px.choropleth_mapbox(df,
                                   title="<b>Somministrazioni prima dose</b>",
                                   geojson=gj, color="percentuale1dose",
                                   locations=df.regione, featureidkey="properties.reg_name",
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map", zoom=4.35,
                                   color_continuous_scale="Viridis",
                                   opacity=0.7)
        fig.update_layout(margin={"r": 0, "t": 25, "l": 0, "b": 0})
        fig.update_layout(title_x=0.5)

        fig2 = px.choropleth_mapbox(df,
                                    title="<b>Somministrazioni seconda dose</b>",
                                    geojson=gj, color="percentuale2dose",
                                    locations=df.regione, featureidkey="properties.reg_name",
                                    center={"lat": 41.902782, "lon": 12.496366},
                                    mapbox_style="open-street-map", zoom=4.35,
                                    color_continuous_scale="Viridis",
                                    opacity=0.7)
        fig2.update_layout(margin={"r": 0, "t": 25, "l": 0, "b": 0})
        fig2.update_layout(title_x=0.5)
        fig.update_layout(coloraxis_showscale=False)
        fig2.update_layout(coloraxis_showscale=False)

        return fig, fig2

