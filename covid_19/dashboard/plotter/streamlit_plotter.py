
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from covid_19.data_manager.plotter.bokeh_plotter import plot_df_lines_bokeh, get_bokeh_plotter
import altair as alt
graph_types = [ "tamponi", "totali_principali", "nuovi_principali", "tassi_principali", "dettaglio_pazienti_attuali", "tassi_condizioni_cliniche"]


def altair_plotter(dataplot):

    source = dataplot.reset_index()


    shown_names = [" ".join(x.split("_")).title() for x in source.columns]

    traduci = {source.columns[i]: shown_names[i] for i in range(len(shown_names))}
    traduci["index"]="Data"
    source = source.rename(columns=traduci)

    source = source.melt('Data', var_name='category', value_name='y')

    hover = alt.selection_single(
        fields=["Data"],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout"
    )

    lines = alt.Chart(source).mark_line().encode(
        x=alt.X('Data:T', title="Data"),
        y=alt.Y('y:Q', title="Andamento"),
        color=alt.Color('category:N', legend=alt.Legend(orient="top", title="Andamenti"))
    )

    points = lines.transform_filter(hover).mark_circle()

    tt = ["Data:T"] + [val + ":Q" for val in shown_names]

    tooltips = alt.Chart(source).transform_pivot(
        "category", "y", groupby=["Data"]
    ).mark_rule().encode(
        x='Data:T',
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=tt
    ).add_selection(hover).properties(height=450).interactive()

    st.altair_chart(lines + points + tooltips, use_container_width=True)


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
        altair_plotter(dataplot)

    elif tipo == "Streamlit":
        st.line_chart(dataplot)

    elif tipo == "Pyplot":
        fig, ax = plt.subplots()
        for colonna in dataplot.columns:
            ax.plot(dataplot.index, dataplot[colonna], label=colonna)

        plt.legend(loc="upper left")
        ax.set(xlabel='data')
        ax.grid()
        plt.xticks(fontsize=8)
        ax.patch.set_alpha(0)
        fig.patch.set_alpha(0)
        st.pyplot(plt)
    expander = st.beta_expander("Mostra Dati")
    expander.write(dataplot)
