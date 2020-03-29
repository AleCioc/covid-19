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


def plot_line_bokeh (df, figures_path, filename, save_flag=False):

    columns_names = list(df.columns)

    if save_flag:
        outfp = os.path.join(
            figures_path,
            filename + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)

    warnings.filterwarnings("ignore")

    df["t"] = df.index.values
    df.t = df.t.apply(lambda d: str(d.date()))
    p = df.plot.line(
        marker="o",
        plot_data_points=True,
        panning=True,
        figsize=(900, 500),
        legend="top_left",
        show_figure=False,
        rangetool=False,
        hovertool_string="""
            t: @t <br/>
        """
    )

    hovers = p.select(dict(type=HoverTool))
    flag_first = True
    for hover in hovers:
        hover.tooltips = []
        if flag_first:
            for y_col in ["t"] + columns_names:
                hover.tooltips += [
                    (y_col, '@{' + y_col + '}'),
                ]
        flag_first = False

    if save_flag:
        item_text = json.dumps(json_item(p, filename))
        output_path = os.path.join(
            figures_path,
            filename + ".json"
        )
        with open(output_path, "w+") as out_f:
            out_f.write(item_text)

        save(p)

    return p


def plot_lines_dashboard(cases_df, figures_path, geo_name, plot_dashboard_flag):

    for save_flag in [True, False]:

        p1 = plot_line_bokeh(
            cases_df[[
                "total_cases",
            ]], figures_path, "cases", save_flag
        )

        p2 = plot_line_bokeh(
            cases_df[[
                "new_currently_positives",
                "total_deaths",
                "total_recovered"
            ]], figures_path, "main_status", save_flag
        )

        p3 = plot_line_bokeh(
            cases_df[[
                "new_positives",
                #"new_currently_positives",
                "new_deaths",
                #"new_recovered"
            ]], figures_path, "main_status", save_flag
        )
        p4 = plot_line_bokeh(
            cases_df[[
                "rate_new_positives",
                "rate_deaths",
                "rate_recovered"
            ]], figures_path, "main_status", save_flag
        )

    if plot_dashboard_flag:
        outfp = os.path.join(
            figures_path,
            geo_name + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)

        plot_grid = pandas_bokeh.plot_grid([
            [p1, p2],
            [p3, p4],
        ], toolbar_location="left")

        pandas_bokeh.save(plot_grid)


def plot_lines_dashboard_ita(cases_df, figures_path, geo_name, plot_dashboard_flag):

    for save_flag in [True, False]:

        p1 = plot_line_bokeh(
            cases_df[[
                "totale_tamponi",
                "totale_casi",
            ]], figures_path, "tamponi", save_flag
        )

        p2 = plot_line_bokeh(
            cases_df[[
                "totale_attualmente_positivi",
                "totale_deceduti",
                "totale_dimessi_guariti"
            ]], figures_path, "totali_principali", save_flag
        )

        p3 = plot_line_bokeh(
            cases_df[[
                "nuovi_positivi",
                "nuovi_attualmente_positivi",
                "nuovi_deceduti",
                "nuovi_dimessi_guariti"
            ]], figures_path, "nuovi_principali", save_flag
        )

        p4 = plot_line_bokeh(
            cases_df[[
                "tasso_positivi_tamponi",
                "tasso_nuovi_positivi",
                "tasso_mortalita",
                "tasso_guarigione"
            ]], figures_path, "tassi_principali", save_flag
        )

        p5 = plot_line_bokeh(
            cases_df[[
                "attualmente_isolamento_domiciliare",
                "attualmente_ricoverati",
                "attualmente_terapia_intensiva",
            ]], figures_path, "dettaglio_pazienti_attuali", save_flag
        )

        p6 = plot_line_bokeh(
            cases_df[[
                "tasso_ricoverati_con_sintomi",
                "tasso_terapia_intensiva",
                "tasso_terapia_intensiva_ricoverati",
            ]], figures_path, "tassi_condizioni_cliniche", save_flag
        )

    if plot_dashboard_flag:
        outfp = os.path.join(
            figures_path,
            geo_name + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)

        plot_grid = pandas_bokeh.plot_grid([
            [p1, p2],
            [p3, p4],
            [p5, p6],
        ], toolbar_location="left")

        pandas_bokeh.save(plot_grid)
