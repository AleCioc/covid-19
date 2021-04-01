
import streamlit as st
from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource
import covid_19.dashboard.dashboard_utils as ut
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

        st.sidebar.title("Seleziona i dati da vedere")
        ds = get_norm_data()

        opzioni = ["Andamento Nazionale", "Andamento Regionale", "Prova long2wide e viceversa"]
        regioni = ["abruzzo", "basilicata", "calabria", "campania", "emilia-romagna", "friuliveneziagiulia", "lazio",
                   "liguria", "lombardia", "marche", "molise", "pabolzano", "patrento", "piemonte",
                   "puglia", "sardegna", "sicilia", "toscana", "umbria", "valledaosta", "veneto"]
        scelta_tipo = st.sidebar.selectbox("Cosa vuoi vedere?", opzioni)

        if scelta_tipo == opzioni[0]:
            scelta_grafico = st.sidebar.selectbox("Quale grafico vuoi vedere?", graph_types)
            show_also_bokeh = st.sidebar.checkbox("Mostra anche grafico con Bokeh")
            ds.plot_dashboard_st(type=scelta_grafico, regione="italia", tipo="Bokeh")

        elif scelta_tipo == opzioni[1]:
            scelta_regione = st.sidebar.selectbox("A quale regione sei interessato?", regioni)
            scelta_grafico = st.sidebar.selectbox("Quale grafico vuoi vedere?", graph_types)
            st.markdown('Stai visualizzando l\'andamento regionale di **' + scelta_regione + '**.')
            show_also_bokeh = st.sidebar.checkbox("Mostra anche grafico con Bokeh")
            ds.plot_dashboard_st(type=scelta_grafico, regione=scelta_regione, tipo="Bokeh")

        elif scelta_tipo == opzioni[2]:
            scelte = ut.determina_scelte(ds.norm_regions_df_ita)
            colonna = st.sidebar.selectbox("Su quale parametro vuoi fare la trasformazione", scelte)
            st.markdown("### Ho questo dataframe in long form")
            st.dataframe(ds.norm_regions_df_ita.head(100))
            st.markdown("### Lo trasformo in wide form interessandomi solo di "+colonna)
            df = ut.long2wide(ds.norm_regions_df_ita, colonna)
            st.dataframe(df.head(100))
            st.markdown("### E ora lo ritrasformo in long form")
            st.dataframe(ut.wide2long(df,colonna).head(100))


