import os

from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from data_manager.config.config import *

from data_manager.plotter.bokeh_plotter import *

italy_cases_ds = ItalyCasesDataSource()
#italy_cases_ds.normalise()
#italy_cases_ds.save_norm()
#italy_cases_ds.load_norm()
#italy_cases_ds.plot_dashboard()

from data_manager.cases_data_source.world_cases_data_source import WorldCasesDataSource
world_cases_ds = WorldCasesDataSource()
world_cases_ds.normalise()
world_cases_ds.save_norm()
#world_cases_ds.load_norm()
#world_cases_ds.normalise()
print(world_cases_ds.top_countries)

#world_cases_ds.plot_country_dashboard("Jordan", True)
#world_cases_ds.plot_country_dashboard("Canada", True)
world_cases_ds.plot_country_dashboard("Italy", True)
#world_cases_ds.plot_country_dashboard("China", True)
#world_cases_ds.plot_country_dashboard("France", True)
#world_cases_ds.plot_country_dashboard("Korea, South", True)
#world_cases_ds.plot_country_dashboard("US", True)
#world_cases_ds.plot_country_dashboard("United Kingdom", True)
#for country in list(world_cases_ds.countries_df_dict.keys()):
#    print(country)
#    world_cases_ds.plot_country_dashboard(country, False)
