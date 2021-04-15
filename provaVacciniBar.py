
from bokeh.io import output_file, show
from bokeh.plotting import figure
import pandas as pd
import streamlit as st
import datetime

data = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/61142006d3ece74fe105ceb91b5a3dfc7260eb37/dati/somministrazioni-vaccini-summary-latest.csv"

df = pd.read_csv(data, index_col=-1)

in_region = df["area"] == "UMB"
after_start_date = df["data_somministrazione"] >= "2021-03-01"
before_end_date = df["data_somministrazione"] <= "2021-03-31"
between_two_dates_and_in = after_start_date & before_end_date & in_region
df = df.loc[between_two_dates_and_in]



df = df.rename(columns={'categoria_operatori_sanitari_sociosanitari': 'Operatori (socio)sanitari',
                        'categoria_personale_non_sanitario': 'Personale non sanitario',
                        "categoria_altro":"Altro",
                        'categoria_ospiti_rsa': "Ospiti RSA",
                        'categoria_over80':"Over 80",
                        "categoria_forze_armate":"Forze armate",
                        "categoria_personale_scolastico":"Personale scolastico"})
st.dataframe(df)
df = df.sort_values("data_somministrazione")


import altair as alt
from vega_datasets import data

source = data.barley()


st.dataframe(source)
small = df[["data_somministrazione","Operatori (socio)sanitari"
            , 'Personale non sanitario', 'Altro',
            'Ospiti RSA', 'Over 80', 'Forze armate', 'Personale scolastico']]
small = small.melt(id_vars='data_somministrazione', var_name='categoria', value_name='numero_vaccini')


st.altair_chart(
    alt.Chart(small).mark_bar().encode(
    x=alt.X('sum(numero_vaccini)', title="Totale dosi somministrate"),
    y=alt.Y('data_somministrazione', title="Data di somministrazione"),
    color=alt.Color('categoria', legend=alt.Legend(title="Categorie", orient="top",titleAlign="left", labelAlign="left", labelFontSize=8)),
    tooltip=["data_somministrazione", "categoria", "numero_vaccini"]
), use_container_width=True)
