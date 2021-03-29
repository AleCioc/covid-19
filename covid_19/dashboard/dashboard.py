
import streamlit as st
from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

graph_types = [ "tamponi", "totali_principali", "nuovi_principali", "tassi_principali", "dettaglio_pazienti_attuali", "tassi_condizioni_cliniche"]


@st.cache(allow_output_mutation=True)
def get_norm_data():
    italy_cases_ds = ItalyCasesDataSource()
    italy_cases_ds.normalise()
    italy_cases_ds.save_norm()
    italy_cases_ds.load_norm()
    return italy_cases_ds


class Dashboard:
    def __init__(self):
        st.title("Covid-19 dashboard")

        st.sidebar.title("Seleziona i dati da vedere")
        ds = get_norm_data()

        opzioni = ["Andamento Nazionale", "Andamento Regionale"]
        regioni = ["abruzzo", "basilicata", "calabria", "campania", "emilia-romagna", "friuliveneziagiulia", "lazio",
                   "liguria", "lombardia", "marche", "molise", "pabolzano", "patrento", "piemonte",
                   "puglia", "sardegna", "sicilia", "toscana", "umbria", "valledaosta", "veneto"]
        scelta_tipo = st.sidebar.selectbox("Cosa vuoi vedere?", opzioni)

        if scelta_tipo == opzioni[0]:
            scelta_grafico = st.sidebar.selectbox("Quale grafico vuoi vedere?", graph_types)
            "\n"
            "Hai selezionato: " + scelta_grafico
            show_also_bokeh = st.sidebar.checkbox("Mostra anche grafico con Bokeh")
            ds.plot_dashboard_st(type=scelta_grafico, regione="italia", show_also_bokeh=show_also_bokeh)

        elif scelta_tipo == opzioni[1]:
            scelta_regione = st.sidebar.selectbox("A quale regione sei interessato?", regioni)
            scelta_grafico = st.sidebar.selectbox("Quale grafico vuoi vedere?", graph_types)
            st.markdown('Stai visualizzando l\'andamento regionale di **' + scelta_regione + '**.')
            show_also_bokeh = st.sidebar.checkbox("Mostra anche grafico con Bokeh")
            ds.plot_dashboard_st(type=scelta_grafico, regione=scelta_regione, show_also_bokeh=show_also_bokeh)


