from functools import partial, partialmethod
import streamlit as st
from covid_19.dashboard_field.dashboard_main import DashboardMain
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.__init__ import create_screens_list
import covid_19.__init__ as start

def main():
       str1 = "Attraverso il menù laterale è possibile scegliere quale tipologia di dati vedere. Si può scegliere un'aggregazione nazionale, regionale" \
              " o confrontare varie regioni tra loro. Ogni schermata mostrerà una serie di grafici ulteriormente personalizzabili. I dati sono presi dalla repo Git" \
              " della Protezione Civile e aggiornati automaticamente alle 18."
       logo = "https://smartdata.polito.it/wp-content/uploads/2017/10/logo_official.png"
       DashboardMain("Benvenuti nella dashboard COVID", create_screens_list(), logo=logo).show()
       #st.sidebar.success("Questa pagina è stata visualizzata " + str(contatore[0]) + " volte!")

main()
