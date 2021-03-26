import streamlit as st
from covid_19.dashboard.dashboard import Dashboard
from covid_19.dashboard.dashaltair import DashboardAltair

st.title("Benvenuti nella dashboard!")
schermate = [ "Grafici classici", "Grafici Altair"]

scelta_schermata = st.sidebar.selectbox("Quale schermata vuoi visualizzare?",schermate)

if scelta_schermata == schermate[0]:
    Dashboard()
elif scelta_schermata == schermate[1]:
    DashboardAltair().stampa()
