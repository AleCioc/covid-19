import os
import warnings

from bokeh.plotting import figure, output_file
import pandas_bokeh
import pandas as pd
pd.set_option('plotting.backend', 'pandas_bokeh')


def plot_line_bokeh (df, figures_path, filename):

    warnings.filterwarnings("ignore")

    outfp = os.path.join(
        figures_path,
        filename + ".html"
    )
    output_file(outfp)
    pandas_bokeh.output_file(outfp)

    p = figure(x_axis_type="datetime")
    p.legend.click_policy="hide"

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
