import datetime
from functools import partial

from covid_19.dashboard_field.dashboard_report import DashboardReport
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.home_page.chart_andamentocolori import ChartAndamentoColori
from covid_19.dashboard_field.home_page.chart_colori import ChartColori
from covid_19.dashboard_field.utils import get_norm_data, transform_regions_pc_to_human_all, determina_scelte, st_functional_columns
from covid_19.dashboard_field.vaccini.chart_barvaccini import ChartBarVaccini
from covid_19.dashboard_field.vaccini.chart_barvacciniitalia import ChartBarVacciniItalia
from covid_19.dashboard_field.vaccini.chart_barvax import ChartBarVax
from covid_19.dashboard_field.vaccini.chart_percentagemap import ChartPercentageMap
from covid_19.dashboard_field.vaccini.chart_pydeckmap import ChartPydeckMap
import streamlit as st

from covid_19.dashboard_field.vaccini.chart_tempform import ChartTempForm


class ScreenHome(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=None, widget_list = None):
        super().__init__(title,name,chart_list,subtitle, widget_list)
        self.data = get_norm_data()

    def show_charts(self):
        self.data = get_norm_data()
        name = "Ultime notizie"
        DashboardReport(name, self.get_last_day(self.data), "italia").show()

        name = "Andamento zone di rischio"
        subtitle = "In questa carta di Gantt è possibile visualizzare l'andamento temporale delle zone di rischio in italia. Passando con" \
                   " il mouse sopra il grafico è possibile vedere la data a cui fan riferimento quei dati."
        dati = "https://raw.githubusercontent.com/imcatta/restrizioni_regionali_covid/main/dataset.csv"

        ChartAndamentoColori(name, name, subtitle, dati).show()

        name = "Zone di rischio in Italia"
        subtitle = "In questa mappa è possibile visualizzare le zone di rischio attualmente in vigore in Italia."
        dati = "https://raw.githubusercontent.com/imcatta/restrizioni_regionali_covid/main/dataset.csv"

        ChartColori(name, name, subtitle, dati).show()




    def get_last_day(self, data):
        df = data.norm_country_df_ita
        return df.iloc[-1]