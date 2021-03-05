
import streamlit as st
from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

@st.cache(allow_output_mutation=True)
def get_norm_data():
    italy_cases_ds = ItalyCasesDataSource()
    italy_cases_ds.normalise()
    italy_cases_ds.save_norm()
    italy_cases_ds.load_norm()
    return italy_cases_ds

