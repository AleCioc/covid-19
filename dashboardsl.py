import streamlit as st
from covid_19.dashboard.dashboard import Dashboard
from covid_19.dashboard.dashaltair import DashboardAltair
import dashboard_script as new

ask = st.sidebar.empty()
versione = ask.checkbox("Versione nuova?", value=False)

print(versione)
if  versione == False:
    st.title("Benvenuti nella dashboard!")
    st.sidebar.image("https://smartdata.polito.it/wp-content/uploads/2017/10/logo_official.png")
    schermate = [ "Grafici classici", "Grafici Altair"]

    scelta_schermata = st.sidebar.selectbox("Quale schermata vuoi visualizzare?",schermate)

    if scelta_schermata == schermate[0]:
        Dashboard()
    elif scelta_schermata == schermate[1]:
        DashboardAltair().stampa()
else:
    new.main()


