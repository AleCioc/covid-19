from covid_19.dashboard_field.andamento_nazionale.chart_standard import ChartStandard
from covid_19.dashboard_field.andamento_nazionale.screen_nazione import ScreenNazione
from covid_19.dashboard_field.andamento_regionale.screen_regione import ScreenRegione
from covid_19.dashboard_field.confronto_regioni.screen_confronti import ScreenConfronti

from covid_19.dashboard_field.dashboard_chart import DashboardChart
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
import streamlit as st
from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource
from covid_19.dashboard_field.utils import *
from functools import partial

@st.cache(allow_output_mutation=True, show_spinner=False)
def create_screens_list():

    sub1 = "In questa schermata puoi visualizzare dati con aggregazione nazionale. Per ogni grafico è riportato il titolo e una breve descrizione. Inoltre, cliccando sull'expander, è possibile visualizzare i dati utilizzati."
    sub2 = "In questa schermata puoi visualizzare dati con aggregazione regionale"
    sub3 = "In questa schermata puoi confrontare i dati di regioni diverse"
    widget_nazione = [partial(st.sidebar.selectbox, "Scegli quale libreria di plotting utilizzare", ["Altair", "Bokeh", "Pyplot"])]
    andamento_nazionale = ScreenNazione("Andamento nazionale", "Andamento nazionale", subtitle=sub1,  widget_list=widget_nazione)
    andamento_regionale = ScreenRegione("Andamento regionale", "Andamento regionale", subtitle=sub2)
    confronti = ScreenConfronti("Confronti tra regioni", "Confronti tra regioni", subtitle=sub3)

    return [andamento_nazionale,andamento_regionale,confronti]


def create_andamentonazionale_charts(tipo="Altair"):
    data = get_norm_data()
    ret = []
    for i in range(len(graph_types)):
        ret.append(ChartStandard(data, graph_types[i], title=graph_titles[i], subtitle=graph_subtitles[i], regione="italia", tipo=tipo))
    return ret

def create_andamentoregionale_charts(regione):
    data = get_norm_data()
    ret = []
    for i in range(len(graph_types)):
        ret.append(ChartStandard(data, graph_types[i], title=graph_titles[i], subtitle=graph_subtitles[i], regione=regione))
    return ret