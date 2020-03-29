import os

from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from data_manager.config.config import *

from data_manager.plotter.bokeh_plotter import *


# italy_cases_ds = ItalyCasesDataSource()
# italy_cases_ds.normalise()
# italy_cases_ds.save_norm()
# #country_df = italy_cases_ds.load_norm()
#
# country_df = italy_cases_ds.norm_country_df_ita.set_index("data")
# regions_df = italy_cases_ds.norm_regions_df_ita.set_index("data")
#
# country_path = os.path.join(
#     italy_figures_path,
#     "country"
# )
# os.makedirs(country_path, exist_ok=True)
# plot_lines_dashboard_ita(country_df, country_path, "country", False)
# for region, df_region in regions_df.groupby("denominazione_regione"):
#     region_path = os.path.join(
#         italy_figures_path,
#         "regions",
#         region
#     )
#     os.makedirs(region_path, exist_ok=True)
#     plot_lines_dashboard_ita(df_region, region_path, region, False)
#

from data_manager.cases_data_source.world_cases_data_source import WorldCasesDataSource
world_cases_ds = WorldCasesDataSource()
#world_cases_ds.normalise()
#world_cases_ds.save_norm()
world_cases_ds.load_norm()
world_cases_ds.normalise()
world_cases_ds.plot_country_dashboard("Armenia")
world_cases_ds.plot_country_dashboard("France")
world_cases_ds.plot_country_dashboard("Italy")
