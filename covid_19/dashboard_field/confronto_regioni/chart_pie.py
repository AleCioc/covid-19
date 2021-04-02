from bokeh.palettes import YlOrBr
from bokeh.plotting import figure
from bokeh.transform import cumsum

from covid_19.dashboard_field.dashboard_chart import DashboardChart
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from covid_19.dashboard_field.utils import transform_region_to_pc, transform_regions_pc_to_human


class ChartPie(DashboardChart):



    def __init__(self, name, title, subtitle, dati, tipo = "Pyplot", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita
        self.tipo = tipo


    def show(self):
        self.show_configuration()

        #come parametri avro' la libreria, il giorno, il parametro da valutare e le regioni
        self.tipo, parametro, giorno, regioni = (self.show_widgets())[0]

        regioni = [ transform_region_to_pc(regione) for regione in regioni ]
        if len(regioni) < 3:
            st.warning("Seleziona almeno tre regioni")
        #prendo solo i dati di quel giorno specifico
        else:
            reduced = self.dati.loc[self.dati["denominazione_regione"].isin(regioni)]
            conta = 0
            data = pd.DataFrame()
            for index, value in reduced.iterrows():
                    tmp = datetime.datetime.fromisoformat(str(value.data))
                    if tmp.month == giorno.month and tmp.year == giorno.year and tmp.day == giorno.day:
                        data = data.append(value)
                        conta+=1

            if self.tipo == "Pyplot":
                self.pie_pyplot(data, parametro)
            elif self.tipo == "Bokeh":
                self.pie_bokeh(data, parametro, regioni)


    def pie_pyplot(self, data, parametro):
        labels = data.denominazione_regione
        sizes = data[parametro]

        fig1, ax1 = plt.subplots()
        wedges, texts = ax1.pie(sizes, wedgeprops=dict(width=0.5), startangle=90)
        titolo = " ".join(parametro.split("_")).capitalize()+"\n\n"
        plt.title(titolo, color="#ee2b33", fontsize=20, fontweight="bold")

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

        ax1.patch.set_alpha(0)
        fig1.patch.set_alpha(0)
        st.pyplot(plt)


    def pie_bokeh(self, data, parametro, regioni):

        regioni = [ transform_regions_pc_to_human(regione) for regione in regioni ]
        elenco = ", ".join(regioni[:-1])+" e "+regioni[-1]+"."
        titolo = " ".join(parametro.split("_")).capitalize() + " nelle regioni " +elenco

        data['angle'] = data[parametro] / data[parametro].sum() * 2 * np.math.pi
        data['color'] = YlOrBr[len(data)]

        p = figure(plot_height=350, title=titolo, toolbar_location=None,
                   tools="hover", tooltips="@denominazione_regione: @"+parametro)

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='denominazione_regione', source=data)
        p.axis.axis_label = None
        p.axis.visible = False
        p.background_fill_alpha = 0
        p.border_fill_alpha = 0
        p.grid.grid_line_color = None
        st.bokeh_chart(p, use_container_width=True)