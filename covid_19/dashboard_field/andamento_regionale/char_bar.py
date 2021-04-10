from bokeh.plotting import figure

from covid_19.dashboard_field.dashboard_chart import DashboardChart
from covid_19.dashboard_field.utils import list_mesi
import datetime
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import bokeh
class ChartBar(DashboardChart):

    def __init__(self, name, title, subtitle, widget_list, dati, regione, tipo):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita.loc[dati.norm_regions_df_ita["denominazione_regione"] == regione]
        self.regione = regione
        self.tipo = tipo


    def show(self):
        self.show_heading()

        #avremo come widget: libreria grafica che arriva dalla regione, il (mese, anno) e il parametro
        ret = self.show_widgets()[0]
        ((mese,anno),parametro) = ret

        data = pd.DataFrame()
        conta = 0
        for index, value in self.dati.iterrows():
                tmp = datetime.datetime.fromisoformat(str(value.data))
                if tmp.month == mese and tmp.year == anno:
                    data = data.append(value)
                    conta += 1

        if self.tipo == "Altair":
            self.barAltair(data, parametro, mese, anno)
        elif self.tipo == "Bokeh":
             self.barBokeh(data, parametro, mese, anno)
        elif self.tipo == "Pyplot":
             self.barPyplot(data, parametro, mese, anno)

    def barAltair(self, data, parametro, mese, anno):
        title = "Andamento "+parametro +" nel mese di " + list_mesi[mese-1] + " " + str(anno)
        st.altair_chart(
            alt.Chart(data, title=title).mark_bar().configure_mark(color="#ee2b33").encode(
                x='data',
                y=parametro
            ), use_container_width=True)

    def barBokeh(self, data, parametro, mese, anno):
        title = "Andamento " + parametro + " nel mese di " + list_mesi[mese - 1] + " " + str(anno)
        p = figure(title=title, plot_height=350, x_axis_type="datetime")
        # Plotting
        p.vbar(data.data,  # categories
               top=data[parametro],  # bar heights
               width=datetime.timedelta(days=0.8),
               fill_alpha=2.5,
               fill_color='#ee2b33',
               line_alpha=2.5,
               line_color='#ee2b33'

               )
        # Signing the axis

        p.xaxis.axis_label = "Data"
        p.yaxis.axis_label = parametro
        p.background_fill_alpha = 0
        p.border_fill_alpha = 0
        st.bokeh_chart(p, use_container_width=True)

    def barPyplot(self, data, parametro, mese, anno):
        fig, ax = plt.subplots()
        title = "Andamento " + parametro + " nel mese di " + list_mesi[mese - 1] + " " + str(anno)

        plt.bar(data.data, data[parametro], color="#ee2b33")
        plt.xticks(data.data, rotation=90, fontsize=6)
        plt.yticks(data[parametro], fontsize=6)  # This may be included or excluded as per need
        plt.xlabel('Data')
        plt.ylabel(parametro)
        plt.title(title, color="#ee2b33", fontsize=10, fontweight="bold")
        ax.patch.set_alpha(0)
        fig.patch.set_alpha(0)
        st.pyplot(plt)




