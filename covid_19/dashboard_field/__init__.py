from covid_19.dashboard_field.andamento_nazionale.chart_standard import ChartStandard
from covid_19.dashboard_field.andamento_regionale.screen_regione import ScreenRegione

from covid_19.dashboard_field.dashboard_chart import DashboardChart
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
import streamlit as st
from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource
from covid_19.dashboard_field.utils import *

@st.cache(allow_output_mutation=True)
def create_screens_list():

    sub1 = "In questa schermata puoi visualizzare dati con aggregazione nazionale. Per ogni grafico è riportato il titolo e una breve descrizione. Inoltre, cliccando sull'expander, è possibile visualizzare i dati utilizzati."
    sub2 = "In questa schermata puoi visualizzare dati con aggregazione regionale"
    sub3 = "In questa schermata puoi confrontare i dati di regioni diverse"
    andamento_nazionale = DashboardScreen("Andamento nazionale", "Andamento nazionale", subtitle=sub1, chart_list=create_andamentonazionale_charts())
    andamento_regionale = ScreenRegione("Andamento regionale", "Andamento regionale", subtitle=sub2)
    confronti = DashboardScreen("Confronti tra regioni", "Confronti tra regioni", subtitle=sub3)

    return [andamento_nazionale,andamento_regionale,confronti]



def create_andamentonazionale_charts():
    data = get_norm_data()
    ret = []
    for i in range(len(graph_types)):
        ret.append(ChartStandard(data, graph_types[i], title=graph_titles[i], subtitle=graph_subtitles[i], regione="italia"))
    return ret

def create_andamentoregionale_charts(regione):
    data = get_norm_data()
    ret = []
    for i in range(len(graph_types)):
        ret.append(ChartStandard(data, graph_types[i], title=graph_titles[i], subtitle=graph_subtitles[i], regione=regione))
    return ret