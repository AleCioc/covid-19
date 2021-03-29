import altair as alt
import streamlit as st
import pandas as pd
from covid_19.dashboard.dashboard import get_norm_data
import geopandas as gpd
import os
import datetime
import matplotlib.pyplot as plt
regioni = ["abruzzo", "basilicata", "calabria", "campania", "emilia-romagna", "friuliveneziagiulia", "lazio",
                   "liguria", "lombardia", "marche", "molise", "pabolzano", "patrento", "piemonte",
                   "puglia", "sardegna", "sicilia", "toscana", "umbria", "valledaosta", "veneto"]

traduci = {"abruzzo":"ABRUZZO", "basilicata":"BASILICATA", "calabria":"CALABRIA", "campania":"CAMPANIA",
           "emilia-romagna":"EMILIA-ROMAGNA", "friuliveneziagiulia":"FRIULI VENEZIA GIULIA", "lazio":"LAZIO",
            "liguria":"LIGURIA", "lombardia":"LOMBARDIA", "marche":"MARCHE", "molise":"MOLISE", "patrento":"TRENTINO-ALTO ADIGE/SUDTIROL",
            "piemonte":"PIEMONTE", "puglia":"PUGLIA", "sardegna":"SARDEGNA", "sicilia":"SICILIA",
           "toscana":"TOSCANA", "umbria":"UMBRIA", "valledaosta":"VALLE D'AOSTA/VALLÉE D'AOSTE VALLE D'AOSTA/VALLÉE D'AOSTE"
                                                                                       , "veneto":"VENETO"}
class DashboardAltair:

    def __init__(self):
        self._data_ = get_norm_data()


    def stampa(self):
        grafico = st.sidebar.selectbox("Quale vista vuoi vedere?", [1,2,3])

        if grafico==1:
            regione = st.sidebar.selectbox("Di quale regione vuoi visualizzare i dati?", regioni)
            self.grafico_didattico_1(self._data_, regione)
        elif grafico==2:
            regione = st.sidebar.selectbox("Di quale regione vuoi visualizzare i dati?", regioni)
            self.grafico_didattico_2(self._data_, regione)
        elif grafico == 3:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            self.grafico_didattico_3()


    def grafico_didattico_1(self,dati, regione):
        data_df = dati.norm_regions_df_ita
        data_df = data_df.loc[ (data_df["denominazione_regione"] == "piemonte") | (data_df["denominazione_regione"] == regione )]

        st.altair_chart(alt.Chart(data_df).mark_point().encode(
            x='data:T',
            y='totale_casi:Q',
            color="denominazione_regione:N"
        ).interactive(), use_container_width=True)

    def grafico_didattico_2(self,dati, regione):
        data_df = dati.norm_regions_df_ita

        min = datetime.datetime.fromisoformat(str(data_df.data.min()))
        max = datetime.datetime.fromisoformat(str(data_df.data.max()))

        (start, stop) = st.slider("Di che periodo?", min_value=min, max_value=max, value=(min,max))

        daStampare = pd.DataFrame()
        data_df_leggero = data_df[["denominazione_regione", "data", "totale_casi"]]
        for key, val in data_df_leggero.iterrows():
            if val["denominazione_regione"] == regione and start <= datetime.datetime.fromisoformat((str(val["data"]))) <= stop:
                daStampare = daStampare.append(val)

        st.altair_chart(alt.Chart(daStampare).mark_point().encode(
            x='data:T',
            y='totale_casi:Q'
        ).interactive(), use_container_width=True)

    def filtra_dati(self, giorno, parametro):
        dati = self._data_.norm_regions_df_ita
        daRitornare = pd.DataFrame()

        for key, val in dati.iterrows():
            data_comoda=datetime.datetime.fromisoformat(str(val.data))
            if data_comoda.day==giorno.day and data_comoda.year==giorno.year and data_comoda.month==giorno.month:
                if val.denominazione_regione != "pabolzano":
                    newData = { "NOME_REG": traduci[val.denominazione_regione],
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

    def grafico_didattico_3(self):
        col1, col2 = st.beta_columns(2)
        min = datetime.datetime.fromisoformat(str(self._data_.norm_regions_df_ita.data.min()))
        max = datetime.datetime.fromisoformat(str(self._data_.norm_regions_df_ita.data.max()))
        giorno = col1.date_input("Seleziona il giorno", min_value=min, max_value=max, value=max)
        gdf = gpd.read_file(os.path.join(os.curdir, "covid_19", "data_manager","italy-with-regions", "reg2011_g.shp"))

        ax = gdf.plot(
            color='white', edgecolor='black')
        gdf.plot(ax=ax, color='red')


        fig, ax = plt.subplots(1, figsize=(15, 15))
        col = "valore"


        scelte_ = list(self._data_.norm_regions_df_ita.columns)[6:]

        scelte = []
        for scelta in scelte_:
            if scelta not in ["note", "note_test", "day_threshold_cases", "note_casi", "codice_nuts_1", "codice_nuts_2"]:
                scelte.append(scelta)

        parametro = col2.selectbox("Scegli quale parametro valutare", scelte)

        ax.set_title(
            parametro,
            fontdict={"fontsize": "35", "fontweight": "3"}, color="Black")

        merge = self.filtra_dati(giorno, parametro)
        merge = gdf.merge(merge, on='NOME_REG', how='right')
        merge.plot(
            ax=ax,
              column=col,
              cmap="OrRd",
              label ="a che serve?",
          legend = True,
          categorical = False
          )
        st.pyplot()


