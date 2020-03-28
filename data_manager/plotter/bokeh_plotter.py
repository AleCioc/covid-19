import os
import warnings
warnings.filterwarnings("ignore")

from bokeh.models import HoverTool
from bokeh.plotting import figure, save, output_file

import pandas_bokeh
import pandas as pd
pd.set_option('plotting.backend', 'pandas_bokeh')


def plot_line_bokeh (df):

    warnings.filterwarnings("ignore")

    p = df.plot.line(
        marker="o",
        plot_data_points=True,
        panning=True,
        figsize=(900, 450),
        legend="top_left",
        show_figure=False,
        rangetool=True,
    )

    return p


def plot_lines_dashboard_ita(cases_df, figures_path, filename):

    outfp = os.path.join(
        figures_path,
        filename + ".html"
    )
    output_file(outfp)
    pandas_bokeh.output_file(outfp)

    p1 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if not col.startswith("nuovi")
            and not col.startswith("tasso")
            and not col.startswith("totale")
            and col not in ["tamponi", "lat", "lon", "codice_regione", "stato"]
        ]],
    )

    p2 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("totale")
        ]],
    )

    p3 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("nuovi")
        ]],
    )

    p4 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("tasso")
        ]],
    )

    plot_grid = pandas_bokeh.plot_grid([
        [p1, p2],
        [p3, p4]
    ])

    pandas_bokeh.save(plot_grid)
