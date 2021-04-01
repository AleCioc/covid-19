from covid_19.dashboard_field.dashboard_chart import DashboardChart
import pandas as pd
import datetime
import streamlit as st
import altair as alt
from covid_19.dashboard_field.utils import list_mesi

class ChartSlider(DashboardChart):

    def __init__(self, name, title, subtitle, widget_list, dati, regione):
        super().__init__(name,title,subtitle,widget_list=widget_list)
        self.dati = dati
        self.regione = regione
        self.origin_subtitle = subtitle


    def show(self):
        self.show_configuration()

        ((start, stop), tipo) = self.show_widgets()
        extra = "Stai visualizzando "+tipo+" nel periodo tra "+str(start.day)+" "+list_mesi[start.month-1]+" "+str(start.year)+" e "+str(stop.day)+" "+list_mesi[stop.month-1]+" "+str(stop.year)+"."
        self.location.markdown("*" +extra+"*")
        daStampare = pd.DataFrame()
        data_df_leggero = self.dati.norm_regions_df_ita[["denominazione_regione", "data", tipo]]

        for key, val in data_df_leggero.iterrows():
            if val["denominazione_regione"] == self.regione and start <= datetime.datetime.fromisoformat(
                    (str(val["data"]))) <= stop:
                daStampare = daStampare.append(val)

        st.altair_chart(alt.Chart(daStampare).mark_point().encode(
            x='data:T',
            y=tipo+':Q'
        ).interactive(), use_container_width=True)



