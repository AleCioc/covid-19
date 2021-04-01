
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from covid_19.data_manager.plotter.bokeh_plotter import plot_df_lines_bokeh, get_bokeh_plotter

graph_types = [ "tamponi", "totali_principali", "nuovi_principali", "tassi_principali", "dettaglio_pazienti_attuali", "tassi_condizioni_cliniche"]


def plot_lines_dashboard_ita_st(cases_df, figures_path, geo_name, plot_dashboard_flag, type, tipo="Altair"):

    if type not in graph_types:
        return

    if type == graph_types[0]:
        dataplot = pd.DataFrame(cases_df, columns=[
                "totale_tamponi",
                "totale_casi",
            ])
    elif type == graph_types[1]:
        dataplot = pd.DataFrame(cases_df, columns=[
                     "totale_attualmente_positivi",
                     "totale_deceduti",
                     "totale_dimessi_guariti"
                 ])
    elif type == graph_types[2]:
        dataplot = pd.DataFrame(cases_df, columns=[
                 "nuovi_positivi",
                 "nuovi_attualmente_positivi",
                 "nuovi_deceduti",
                 "nuovi_dimessi_guariti"
             ])
    elif type == graph_types[3]:
        dataplot = pd.DataFrame(cases_df, columns=[
            "tasso_positivi_tamponi",
                 "tasso_nuovi_positivi",
                 "tasso_mortalita",
                 "tasso_guarigione"
        ])
    elif type == graph_types[4]:
        dataplot = pd.DataFrame(cases_df, columns=[
            "attualmente_isolamento_domiciliare",
            "attualmente_ricoverati",
            "attualmente_terapia_intensiva"
        ])
    elif type == graph_types[5]:
        dataplot = pd.DataFrame(cases_df, columns=[
            "tasso_ricoverati_con_sintomi",
            "tasso_terapia_intensiva",
            "tasso_terapia_intensiva_ricoverati",
        ])


    dataplot.set_index(cases_df["data"], inplace=True)


    if tipo == "Bokeh":
        st.bokeh_chart(get_bokeh_plotter(cases_df, figures_path, geo_name, plot_dashboard_flag, type), use_container_width=True)
    elif tipo == "Altair":
        st.line_chart(dataplot)
    elif tipo == "Plotly":
        fig, ax = plt.subplots()
        for colonna in dataplot.columns:
            ax.plot(dataplot.index, dataplot[colonna], label=colonna)

        plt.legend(loc="upper left")
        ax.set(xlabel='data')
        ax.grid()
        st.pyplot(plt)
    expander = st.beta_expander("Mostra Dati")
    expander.write(dataplot)
