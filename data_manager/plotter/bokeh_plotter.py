import os
import warnings
warnings.filterwarnings("ignore")
import itertools
import json

import pandas as pd
from bokeh.models import HoverTool
from bokeh.plotting import figure, save, output_file
from bokeh.embed import json_item

import pandas_bokeh
pd.set_option('plotting.backend', 'pandas_bokeh')


def plot_line_bokeh (df, figures_path, filename):

    outfp = os.path.join(
        figures_path,
        filename + ".html"
    )
    output_file(outfp)
    pandas_bokeh.output_file(outfp)

    warnings.filterwarnings("ignore")

    p = df.plot.line(
        marker="o",
        plot_data_points=True,
        panning=True,
        figsize=(1200, 500),
        legend="top_left",
        show_figure=False,
        rangetool=True,
    )

    item_text = json.dumps(json_item(p, filename))
    output_path = os.path.join(
        figures_path,
        filename + ".json"
    )
    with open(output_path, "w+") as out_f:
        out_f.write(item_text)

    save(p)

    return p


def plot_lines_dashboard_ita(cases_df, figures_path):

    p1 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("attualmente")
        ]], figures_path, "attualmente"
    )

    p2 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("totale")
        ]], figures_path, "totale"
    )

    p3 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("nuovi")
        ]], figures_path, "nuovi"
    )

    p4 = plot_line_bokeh(
        cases_df[[
            col for col in cases_df
            if col.startswith("tasso")
        ]], figures_path, "tasso"
    )

