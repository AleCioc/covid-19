import streamlit as st
from covid_19.dashboard.dashboard import get_norm_data


graph_types = [ "tamponi", "totali_principali", "nuovi_principali", "tassi_principali", "dettaglio_pazienti_attuali", "tassi_condizioni_cliniche"]

st.title("Covid-19 dashboard")


ds = get_norm_data()

scelta_grafico = st.sidebar.selectbox("Quale grafico vuoi vedere?",graph_types)

"\n"
"Hai selezionato: "+scelta_grafico

ds.plot_dashboard_st(type=scelta_grafico)
