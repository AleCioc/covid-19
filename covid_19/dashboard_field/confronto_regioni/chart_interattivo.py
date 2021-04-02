from covid_19.dashboard_field.dashboard_chart import DashboardChart
import altair as alt
import streamlit as st
from covid_19.dashboard_field.utils import transform_region_to_pc

class ChartInterattivo(DashboardChart):

    def __init__(self, name, title, subtitle, dati, tipo = "Altair", widget_list=None):
        super().__init__(name, title, subtitle, widget_list=widget_list)
        self.dati = dati.norm_regions_df_ita
        self.tipo = tipo


    def show(self):
        self.show_configuration()

        #come parametri avro' una lista di regioni e il parametro da valutare
        a = (self.show_widgets())[0]
        (regioni, par) = a

        #ritrasformo le regioni

        regioni = [ transform_region_to_pc(regione) for regione in regioni ]

        if len(regioni) < 1:
            st.warning("Seleziona almeno una regione")

        else:
            source = self.dati.loc[self.dati["denominazione_regione"].isin(regioni)]

            brush = alt.selection(type='interval')

            titolo = par.split("_")
            titolo = " ".join(titolo)
            points = alt.Chart(source).mark_point().encode(
                x=alt.X('data:T', axis=alt.Axis(title="data")),
                y=alt.Y(par, axis=alt.Axis(title=titolo)),
                color=alt.condition(brush, 'denominazione_regione:N', alt.value('lightgray'), legend=None)
            ).add_selection(
                brush
            )

            bars = alt.Chart(source).mark_bar().encode(
                x=alt.X('max('+par+'):Q', axis=alt.Axis(title="Massimo di "+titolo)),
                y=alt.Y('denominazione_regione', axis=alt.Axis(title="Denominazione della regione")),
                color='denominazione_regione:N'
            ).transform_filter(
                brush
            ).interactive()

            st.altair_chart(points & bars, use_container_width=True)

