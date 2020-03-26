import os

from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from data_manager.config.config import *

from data_manager.plotter.bokeh_plotter import *


italy_cases_ds = ItalyCasesDataSource()
italy_cases_ds.normalise()
italy_cases_ds.save_norm()
country_df = italy_cases_ds.norm_country_df_ita
#country_df = italy_cases_ds.load_norm()

plot_line_bokeh(
    country_df.set_index("data")[[
        'tamponi',
        'totale_casi',
    ]],
    root_figures_path,
    "tamponi_casi"
)

plot_line_bokeh(
    country_df.set_index("data")[[
        'nuovi_attualmente_positivi',
        'nuovi_positivi_totali',
    ]],
    root_figures_path,
    "nuovi_positivi"
)
