import streamlit as st
from covid_19.dashboard_field.dashboard_main import DashboardMain
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.__init__ import create_screens_list


def main():
       prima_volta=inizializza()


       str1 = "Attraverso il menù laterale è possibile scegliere quale tipologia di dati vedere. Si può scegliere un'aggregazione nazionale, regionale" \
              " o confrontare varie regioni tra loro. Ogni schermata mostrerà una serie di grafici ulteriormente personalizzabili. I dati sono presi dalla repo Git" \
              " della Protezione Civile e aggiornati automaticamente alle 18."
       logo = "https://smartdata.polito.it/wp-content/uploads/2017/10/logo_official.png"
       home = DashboardMain("Benvenuti nella dashboard COVID", create_screens_list(), logo=logo)
       home.show_configuration()
       if prima_volta[0] == False:
              st.success(str1)
              prima_volta[0]=True
       scelto = home.show_widgets()
       home.show_screen(scelto)

@st.cache(allow_output_mutation=True)
def inizializza():
       return  [False]

main()
