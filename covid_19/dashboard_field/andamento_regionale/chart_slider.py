from bokeh.plotting import figure

from covid_19.dashboard_field.dashboard_chart import DashboardChart
import pandas as pd
import datetime
import streamlit as st
import altair as alt
from covid_19.dashboard_field.utils import list_mesi
import matplotlib.pyplot as plt

class ChartSlider(DashboardChart):

    def __init__(self, name, title, subtitle, widget_list, dati, regione, tipo = "Altair"):
        super().__init__(name,title,subtitle,widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita.loc[dati.norm_regions_df_ita["denominazione_regione"] == regione]
        self.regione = regione
        self.tipo = tipo




    def show(self):
        self.show_configuration()


        a = (self.show_widgets())[0]
        ((start, stop), dummy, par) = a

        extra = "Stai visualizzando " + par + " nel periodo tra " + str(start.day) + " " + list_mesi[
            start.month - 1] + " " + str(start.year) + " e " + str(stop.day) + " " + list_mesi[
                    stop.month - 1] + " " + str(stop.year) + "."
        self.location.markdown("*" + extra + "*")
        daStampare = pd.DataFrame()
        data_df_leggero = self.dati[["data", par]]

        for key, val in data_df_leggero.iterrows():
            if  start <= datetime.datetime.fromisoformat(
                    (str(val["data"]))) <= stop:
                daStampare = daStampare.append(val)

        if self.tipo == "Altair":
            self.chartAltair(daStampare,par)
        elif self.tipo == "Bokeh":
            self.chartBokeh(daStampare,par)
        elif self.tipo == "Pyplot":
            self.chartPyplot(daStampare,par)





    def chartAltair(self, data, par):
        st.altair_chart(alt.Chart(data).mark_point().encode(
            x='data:T',
            y=par + ':Q'
        ).interactive(), use_container_width=True)

    def chartBokeh(self, data, par):
        p = figure( x_axis_label='data', y_axis_label=par, x_axis_type="datetime")
        p.line(data.data, data[par], legend_label=par, line_width=2)
        p.background_fill_alpha = 0
        p.border_fill_alpha = 0
        st.bokeh_chart(p, use_container_width=True)

    def chartPyplot(self, data, par):
        fig, ax = plt.subplots()

        ax.plot(data.data, data[par])

        ax.set(xlabel='data', ylabel=par)

        ax.patch.set_alpha(0)
        fig.patch.set_alpha(0)
        ax.grid()
        st.pyplot(plt)
