import math

import altair as alt
import streamlit as st
import pandas as pd
from covid_19.dashboard.dashboard import get_norm_data
import geopandas as gpd
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from covid_19.dashboard.dashboard_utils import determina_scelte
from bokeh.palettes import YlOrBr
from bokeh.plotting import figure
from bokeh.transform import cumsum
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
        self.scelte = ["Confronto tra regioni", "Intervallo temporale", "Mappe", "Confronto interattivo", "Totale cumulato",
                       "Confronto lineplot", "Confronto istogrammi", "Confronto pie chart"]


    def stampa(self):
        grafico = st.sidebar.selectbox("Quale vista vuoi vedere?", self.scelte)

        if grafico==self.scelte[0]:
            regione1 = st.sidebar.selectbox("Di quale regione vuoi visualizzare i dati?", regioni)
            regione2 = st.sidebar.selectbox("Scegli l'altra per confrontarli", regioni)
            if regione1 == regione2:
                st.sidebar.warning("Stai confrontando la stessa regione. Riprova selezionando due regioni diverse")
            else:
                st.write("\n Stai confrontando l'andamento di "+regione1+" con quello di "+regione2+".\n\n")
                self.grafico_didattico_1(self._data_, regione1, regione2)
        elif grafico==self.scelte[1]:
            regione = st.sidebar.selectbox("Di quale regione vuoi visualizzare i dati?", regioni)
            self.grafico_didattico_2(self._data_, regione)
        elif grafico == self.scelte[2]:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            self.grafico_didattico_3()
        elif grafico == self.scelte[3]:
            regione = st.sidebar.multiselect("Di quale regione vuoi visualizzare i dati?", regioni)
            self.grafico_didattico_4( regione)
        elif grafico == self.scelte[4]:
            self.grafico_didattico_5()
        elif grafico == self.scelte[5]:
            self.confronto_lineplot()
        elif grafico == self.scelte[6]:
            self.confronto_istogrammi()
        elif grafico == self.scelte[7]:
            self.confronto_piecharts()

    def grafico_didattico_1(self,dati, regione1,regione2):
        data_df = dati.norm_regions_df_ita
        data_df = data_df.loc[ (data_df["denominazione_regione"] == regione1) | (data_df["denominazione_regione"] == regione2 )]

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


        scelte_ = determina_scelte(self._data_.norm_regions_df_ita)

        parametro = col2.selectbox("Scegli quale parametro valutare", scelte_)

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




    def grafico_didattico_4(self, regione):

        source = self._data_.norm_regions_df_ita

        source = source.loc[ source["denominazione_regione"].isin(regione)]

        brush = alt.selection(type='interval')

        points = alt.Chart(source).mark_point().encode(
            x='data:T',
            y='totale_casi:Q',
            color=alt.condition(brush, 'denominazione_regione:N', alt.value('lightgray'))
        ).add_selection(
            brush
        )

        bars = alt.Chart(source).mark_bar().encode(
            y='denominazione_regione:N',
            color='denominazione_regione:N',
            x='max(totale_casi):Q'
        ).transform_filter(
            brush
        ).interactive()

        st.altair_chart(points & bars)

    def grafico_didattico_5(self):
        st.balloons()
        source = self._data_.norm_regions_df_ita.loc[self._data_.norm_regions_df_ita.denominazione_regione=="piemonte"]

        base = alt.Chart(source).mark_area(
            color='goldenrod',
            opacity=0.3
        ).encode(
            x='data:T',
            y='totale_casi:Q',
        )

        brush = alt.selection_interval(encodings=['x'], empty='all')
        background = base.add_selection(brush)
        selected = base.transform_filter(brush).mark_area(color='goldenrod')


        st.altair_chart(background + selected)

    def confronto_lineplot(self):
        st.markdown("### Confronto tra grafici in bokeh, matplotlib e altair")
        regione = st.sidebar.selectbox("Scegli una regione", regioni)

        data = self._data_.norm_regions_df_ita.loc[ self._data_.norm_regions_df_ita.denominazione_regione == regione ]

        #Matplotlib
        st.markdown("## Versione con Matplotlib")
        fig, ax = plt.subplots()

        ax.plot(data.data, data.totale_casi)

        ax.set(xlabel='data', ylabel='totale casi ',
               title='Grafico con Matplotlib')
        ax.grid()
        st.pyplot(plt)

        #Altair
        st.markdown("## Versione con Altair")
        st.altair_chart(
            alt.Chart(data, title="Grafico con Altair").mark_line().encode(
            x='data',
            y='totale_casi'
        ).interactive(), use_container_width=True)

        #Bokeh
        st.markdown("## Versione con Bokeh")
        p = figure(title="Grafico con Bokeh", x_axis_label='data', y_axis_label='totale_casi',x_axis_type="datetime" )
        p.line(data.data, data.totale_casi, legend_label="Totale casi", line_width=2)

        st.bokeh_chart(p, use_container_width=True)

    def confronto_istogrammi(self):
        st.markdown("### Confronto tra grafici in bokeh, matplotlib e altair")

        mesi_disponibili = [
            (3,2020), (4,2020), (5,2020), (6,2020), (7,2020), (8,2020), (9,2020), (10,2020),
            (11, 2020), (12,2020), (1,2021), (2,2021), (3,2021)
        ]


        mese = st.sidebar.selectbox("Scegli un mese", mesi_disponibili)
        regione = st.sidebar.selectbox("Scegli una regione", regioni)

        #prendo solo i dati di quel mese specifico
        data = pd.DataFrame()
        conta = 0
        for index, value in self._data_.norm_regions_df_ita.iterrows():
            if regione == value.denominazione_regione:
                tmp = datetime.datetime.fromisoformat(str(value.data))
                if tmp.month == mese[0] and tmp.year == mese[1]:
                    data = data.append(value)
                    conta+=1


        #Matplotlib
        st.markdown("## Versione con Matplotlib")

        fig, ax = plt.subplots()

        plt.bar(data.data, data.nuovi_positivi, color = "#ee2b33")
        plt.xticks(data.data, rotation = 90, fontsize=6)
        plt.yticks(data.nuovi_positivi, fontsize=6)  # This may be included or excluded as per need
        plt.xlabel('Data')
        plt.ylabel('Nuovi positivi')
        plt.title("Istogramma con matplotlib", color = "#ee2b33", fontsize=20, fontweight = "bold")

        st.pyplot(plt)

        #Altair

        st.markdown("## Versione con Altair")
        st.altair_chart(alt.Chart(data, title="Istogramma con Altair").mark_bar().configure_mark(color = "#ee2b33").encode(
            x='data',
            y='nuovi_positivi'

        ), use_container_width=True)
        #Bokeh
        st.markdown("## Versione con Bokeh")

        p = figure(title="Istogramma con Bokeh", plot_height=350, x_axis_type="datetime")
        # Plotting
        p.vbar(data.data,  # categories
               top=data.nuovi_positivi,  # bar heights
               width=datetime.timedelta(days=0.8),
               fill_alpha=2.5,
               fill_color='#ee2b33',
               line_alpha=2.5,
               line_color='#ee2b33'

               )
        # Signing the axis

        p.xaxis.axis_label = "Data"
        p.yaxis.axis_label = "Nuovi positivi"
        st.bokeh_chart(p, use_container_width=True)

    def confronto_piecharts(self):
        st.markdown("### Confronto tra grafici in bokeh, matplotlib e altair")
        col1, col2 = st.beta_columns(2)
        min = datetime.datetime.fromisoformat(str(self._data_.norm_regions_df_ita.data.min()))
        max = datetime.datetime.fromisoformat(str(self._data_.norm_regions_df_ita.data.max()))
        giorno = col1.date_input("Seleziona il giorno", min_value=min, max_value=max, value=max)
        regioni_scelte = col2.multiselect("Quali regioni vuoi analizzare?", regioni)

        if len(regioni_scelte) < 3:
            st.warning("Seleziona almeno tre regioni")
        #prendo solo i dati di quel giorno specifico
        else:
            data = pd.DataFrame()
            conta = 0
            for index, value in self._data_.norm_regions_df_ita.iterrows():
                    tmp = datetime.datetime.fromisoformat(str(value.data))
                    if tmp.month == giorno.month and tmp.year == giorno.year and tmp.day == giorno.day\
                            and value.denominazione_regione in regioni_scelte:
                        data = data.append(value)
                        conta+=1


            #Matplotlib
            st.markdown("## Versione con Matplotlib")

            labels = data.denominazione_regione
            sizes = data.nuovi_positivi

            fig1, ax1 = plt.subplots()
            wedges, texts = ax1.pie(sizes, wedgeprops=dict(width=0.5), startangle=90)
            #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


            plt.title("Pie chart con matplotlib\n\n", color="#ee2b33", fontsize=20, fontweight="bold")


            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            kw = dict(arrowprops=dict(arrowstyle="-"),
                      bbox=bbox_props, zorder=0, va="center")

            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1) / 2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                ax1.annotate(data.iloc[i].denominazione_regione, xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                            horizontalalignment=horizontalalignment, **kw)


            st.pyplot(plt)

            #Altair

            st.markdown("## Altair non supporta i Pie chart :(")

            #Bokeh
            st.markdown("## Versione con Bokeh")

            data['angle'] = data['nuovi_positivi'] / data['nuovi_positivi'].sum() * 2 * math.pi
            data['color'] = YlOrBr[len(data)]

            p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
                       tools="hover", tooltips="@denominazione_regione: @nuovi_positivi")

            p.wedge(x=0, y=1, radius=0.4,
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                    line_color="white", fill_color='color', legend='denominazione_regione', source=data)
            p.axis.axis_label = None
            p.axis.visible = False
            p.grid.grid_line_color = None
            st.bokeh_chart(p, use_container_width=True)
