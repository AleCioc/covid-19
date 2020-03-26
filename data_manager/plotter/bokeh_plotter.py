import os
import warnings
warnings.filterwarnings("ignore")

from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, MultiPolygons,
                          GeoJSONDataSource, HoverTool, LogColorMapper,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure, save, output_file, output_notebook, show
import pandas_bokeh


def plot_line_bokeh (df, figures_path, filename):
    outfp = os.path.join(
        figures_path,
        filename + ".html"
    )
    output_file(outfp)
    pandas_bokeh.output_file(outfp)
    warnings.filterwarnings("ignore")
    p = figure(x_axis_type="datetime")
    p = df.plot_bokeh(
        kind="line",
        marker="o",
        plot_data_points=True,
        panning=False,
        figsize=(900, 450),
        legend = "top_left"
    )
    p.legend.click_policy="hide"


