import os
import warnings
warnings.filterwarnings("ignore")
from bokeh.plotting import figure, save, output_file
import pandas_bokeh
import pandas as pd
pd.set_option('plotting.backend', 'pandas_bokeh')


def plot_line_bokeh (df):

    warnings.filterwarnings("ignore")

    p = figure(x_axis_type="datetime")
    p.legend.click_policy="hide"
    print(df.index)
    p = df.plot_bokeh(
        kind="line",
        marker="o",
        plot_data_points=True,
        panning=False,
        figsize=(900, 450),
        legend="top_left",
        show_figure=False
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
        cases_df.set_index("data")[[
            'tamponi',
            'totale_casi',
        ]],
    )

    p2 = plot_line_bokeh(
        cases_df.set_index("data")[[
            'nuovi_attualmente_positivi',
            'nuovi_positivi_totali',
        ]],
    )

    plot_grid = pandas_bokeh.plot_grid([
        [p1, p2],
    ])

    pandas_bokeh.save(plot_grid)
