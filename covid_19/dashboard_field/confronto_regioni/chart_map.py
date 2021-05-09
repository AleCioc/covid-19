from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import datetime
import geopandas as gpd
import matplotlib.pyplot as plt
from covid_19.dashboard_field.utils import determina_scelte
import os
import pandas as pd


class ChartMap(DashboardChart):

    def __init__(self, name, title, subtitle, dati, tipo = "Pyplot", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita
        self.tipo = tipo

        self.traduci = {"abruzzo": "ABRUZZO", "basilicata": "BASILICATA", "calabria": "CALABRIA", "campania": "CAMPANIA",
               "emilia-romagna": "EMILIA-ROMAGNA", "friuliveneziagiulia": "FRIULI VENEZIA GIULIA", "lazio": "LAZIO",
               "liguria": "LIGURIA", "lombardia": "LOMBARDIA", "marche": "MARCHE", "molise": "MOLISE",
               "patrento": "TRENTINO-ALTO ADIGE/SUDTIROL",
               "piemonte": "PIEMONTE", "puglia": "PUGLIA", "sardegna": "SARDEGNA", "sicilia": "SICILIA",
               "toscana": "TOSCANA", "umbria": "UMBRIA",
               "valledaosta": "VALLE D'AOSTA/VALLÉE D'AOSTE VALLE D'AOSTA/VALLÉE D'AOSTE"
        , "veneto": "VENETO"}

    def show(self):
        self.show_heading()

        #come parametri avro' parametro da valutare e il giorno
        giorno, parametro = (self.show_widgets())[0]


        gdf = gpd.read_file(os.path.join(os.curdir, "covid_19", "data_manager", "italy-with-regions", "reg2011_g.shp"))

        ax = gdf.plot(
            color='white', edgecolor='black')
        gdf.plot(ax=ax, color='red')

        fig, ax = plt.subplots(1, figsize=(15, 15))
        col = "valore"

        ax.set_title(
            " ".join(parametro.split("_")).capitalize(),
            fontdict={"fontsize": "32", "fontweight": "3"}, color="Black")

        merge = self.filtra_dati(giorno, parametro)
        merge = gdf.merge(merge, on='NOME_REG', how='right')
        merge.plot(
            ax=ax,
            column=col,
            cmap="OrRd",
            label="a che serve?",
            legend=True,
            categorical=False
        )
        ax.patch.set_alpha(0)
        fig.patch.set_alpha(0)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    def filtra_dati(self, giorno, parametro):
        dati = self.dati
        daRitornare = pd.DataFrame()

        for key, val in dati.iterrows():
            data_comoda=datetime.datetime.fromisoformat(str(val.data))
            if data_comoda.day==giorno.day and data_comoda.year==giorno.year and data_comoda.month==giorno.month:
                if val.denominazione_regione != "pabolzano":
                    newData = { "NOME_REG": self.traduci[val.denominazione_regione],
                                "valore":val[parametro]}
                    newData = pd.Series(newData)
                    daRitornare = daRitornare.append(newData, ignore_index=True)
                else:
                    a_parte = val
        if len(daRitornare) == 0:
            raise ValueError("Data non disponibile")
        #bisogna gestire bolzano
        daRitornare.loc[daRitornare.NOME_REG == "TRENTINO-ALTO ADIGE/SUDTIROL", "valore"] += a_parte[parametro]
        if "tasso" in parametro:
            daRitornare.loc[daRitornare.NOME_REG == "TRENTINO-ALTO ADIGE/SUDTIROL", "valore"] *= 0.5
        return daRitornare