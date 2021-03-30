import streamlit as st
import pandas as pd
def wide2long(wide, values, columns='denominazione_regione'):
    return wide.melt('data', var_name=columns, value_name=values)

def long2wide(long, values, columns="denominazione_regione"):
    return long.pivot(index='data', columns=columns, values=values).reset_index()

@st.cache
def determina_scelte(dati):
    scelte_ = list(dati)[6:]
    scelte_ret = []
    for scelta in scelte_:
        if scelta not in ["note", "note_test", "day_threshold_cases", "note_casi", "codice_nuts_1", "codice_nuts_2"]:
                scelte_ret.append(scelta)
    return scelte_ret