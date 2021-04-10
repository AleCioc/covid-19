import geojson
import plotly.express as px
from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import datetime
from covid_19.dashboard_field.utils import determina_scelte
import os
import pandas as pd


class ChartMapPlotly(DashboardChart):

    def __init__(self, name, title, subtitle, dati, tipo = "Pyplot", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita
        self.tipo = tipo

        self.traduci_geojson = { "piemonte":'Piemonte', "valledaosta":"Valle d'Aosta/Vallée d'Aoste", "lombardia":'Lombardia',
                    "patrento":'Trentino-Alto Adige/Südtirol', "veneto":'Veneto', "friuliveneziagiulia":'Friuli-Venezia Giulia',
                    "liguria":'Liguria', "emilia-romagna":'Emilia-Romagna', "toscana":'Toscana', "umbria":'Umbria',
                    "marche":'Marche', "lazio":'Lazio', "abruzzo":'Abruzzo', "molise":'Molise', "campania":'Campania',
                    "puglia":'Puglia', "basilicata":'Basilicata', "calabria":'Calabria', "sicilia":'Sicilia', "sardegna":'Sardegna'}


    def show(self):
        self.show_heading()

        #come parametri avro' parametro da valutare e il giorno
        giorno, parametro = (self.show_widgets())[0]

        with open(os.path.join(os.curdir, "covid_19", "data_manager", "limits_IT_regions.geojson"), encoding="utf-8") as f:
            gj = geojson.load(f)

        #regioni = [gj["features"][i]["properties"]["reg_name"] for i in range(20)]
        #print(regioni)
        df = self.filtra_dati_json(giorno, parametro)
        fig = px.choropleth_mapbox(df, geojson=gj, color=parametro,
                                   locations=df.NOME_REG, featureidkey="properties.reg_name",
                                   center={"lat": 41.902782, "lon": 12.496366},
                                   mapbox_style="open-street-map", zoom=4.35,
                                   color_continuous_scale="Viridis",
                                   opacity=0.7)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    @st.cache
    def filtra_dati_json(self, giorno, parametro):
        dati = self.dati
        daRitornare = pd.DataFrame()

        for key, val in dati.iterrows():
            data_comoda = datetime.datetime.fromisoformat(str(val.data))
            if data_comoda.day == giorno.day and data_comoda.year == giorno.year and data_comoda.month == giorno.month:
                if val.denominazione_regione != "pabolzano":
                    newData = {"NOME_REG": self.traduci_geojson[val.denominazione_regione],
                               parametro: val[parametro]}
                    newData = pd.Series(newData)
                    daRitornare = daRitornare.append(newData, ignore_index=True)
                else:
                    a_parte = val
        if len(daRitornare) == 0:
            raise ValueError("Data non disponibile")
        # bisogna gestire bolzano
        daRitornare.loc[daRitornare.NOME_REG == "Trentino-Alto Adige/SÃ¼dtirol", parametro] += a_parte[parametro]
        if "tasso" in parametro:
            daRitornare.loc[daRitornare.NOME_REG == "TRENTINO-ALTO ADIGE/SUDTIROL", parametro] *= 0.5
        return daRitornare



