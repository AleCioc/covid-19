
from bokeh.io import output_file, show
from bokeh.plotting import figure
import pandas as pd
import streamlit as st
import datetime

data = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv"

df = pd.read_csv(data, index_col=-1)

after_start_date = df["data_somministrazione"] >= "2021-04-01"
before_end_date = df["data_somministrazione"] <= "2021-05-31"
between_two_dates_and_in = after_start_date & before_end_date
df = df.loc[between_two_dates_and_in]



df = df.rename(columns={'categoria_operatori_sanitari_sociosanitari': 'Operatori (socio)sanitari',
                        'categoria_personale_non_sanitario': 'Personale non sanitario',
                        "categoria_altro":"Altro",
                        'categoria_ospiti_rsa': "Ospiti RSA",
                        'categoria_over80':"Over 80",
                        "categoria_forze_armate":"Forze armate",
                        "categoria_personale_scolastico":"Personale scolastico",
                        "categoria_soggetti_fragili":"Soggetti fragili",
                        "categoria_60_69":"60-69",
                        "categoria_70_79":"70-79"})
st.dataframe(df)
df = df.sort_values("data_somministrazione")


import altair as alt


st.dataframe(df)

small = df[["data_somministrazione","Operatori (socio)sanitari"
            , 'Personale non sanitario', 'Altro',
            'Ospiti RSA', 'Over 80', 'Forze armate', 'Personale scolastico', "Soggetti fragili", "60-69", "70-79"]]
small = small.melt(id_vars='data_somministrazione', var_name='categoria', value_name='numero_vaccini')

st.altair_chart(
    alt.Chart(small).mark_bar().encode(
    x=alt.X('sum(numero_vaccini)', title="Totale dosi somministrate"),
    y=alt.Y('data_somministrazione', title="Data di somministrazione"),
    color=alt.Color('categoria', legend=alt.Legend(title="Categorie", orient="right",titleAlign="left", labelAlign="left", labelFontSize=8)),
    tooltip=["data_somministrazione", "categoria", "numero_vaccini"]
), use_container_width=True)
