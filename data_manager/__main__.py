import os

from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from data_manager.config.config import *

from data_manager.plotter.bokeh_plotter import *


italy_cases_ds = ItalyCasesDataSource()
italy_cases_ds.normalise()
italy_cases_ds.save_norm()
country_df = italy_cases_ds.norm_country_df_ita
#country_df = italy_cases_ds.load_norm()

plot_country_dashboard_ita(country_df, root_figures_path, "dashboard_italia")
