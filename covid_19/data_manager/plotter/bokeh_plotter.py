import os
import warnings

warnings.filterwarnings("ignore")
import itertools
import json

import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, Line, Plot, Grid, LinearAxis
from bokeh.plotting import curdoc, figure, save, show, output_file
from bokeh.embed import json_item
from bokeh.palettes import Dark2_5
import pandas_bokeh

graph_types = [ "tamponi", "totali_principali", "nuovi_principali", "tassi_principali", "dettaglio_pazienti_attuali", "tassi_condizioni_cliniche"]


pd.set_option('plotting.backend', 'pandas_bokeh')


def plot_comparison_df_bokeh(
        df, y_cols,
        figures_path,
        filename,
        save_flag=False
):
    columns_names = list(df.columns)

    if save_flag:
        outfp = os.path.join(
            figures_path,
            filename + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)

    warnings.filterwarnings("ignore")

    df.index.name = "t"

    p = df.plot.line(
        marker="o",
        plot_data_points=True,
        panning=True,
        figsize=(1200, 600),
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
            for y_col in df.columns:
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


def plot_df_lines_bokeh(
        df, x_col, y_cols,
        figures_path,
        filename,
        save_flag=False
):
    columns_names = list(df.columns)

    if save_flag:
        outfp = os.path.join(
            figures_path,
            filename + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)

    warnings.filterwarnings("ignore")

    df = df.set_index(x_col, drop=True)[y_cols]
    df["t"] = df.index.values
    if x_col == "data" or x_col == "datetime":
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
            for y_col in ["t"] + y_cols:
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
    if plot_dashboard_flag:

        save_flag = False

        outfp = os.path.join(
            figures_path,
            geo_name + ".html"
        )
        output_file(outfp)
        pandas_bokeh.output_file(outfp)
    else:
        save_flag = True

    p1 = plot_df_lines_bokeh(
        cases_df, "datetime", [
            "total_cases",
        ], figures_path, "cases", save_flag
    )

    p2 = plot_df_lines_bokeh(
        cases_df, "datetime", [
            "total_deaths",
            "total_recovered"
        ], figures_path, "main_totals", save_flag
    )

    p3 = plot_df_lines_bokeh(
        cases_df, "datetime", [
            "new_positives",
            "new_currently_positives",
            "new_deaths",
            "new_recovered"
        ], figures_path, "main_new", save_flag
    )
    p4 = plot_df_lines_bokeh(
        cases_df, "datetime", [
            "rate_new_positives",
            "rate_deaths",
            "rate_recovered"
        ], figures_path, "main_rate", save_flag
    )

    if plot_dashboard_flag:
        plot_grid = pandas_bokeh.plot_grid([
            [p1, p2],
            [p3, p4],
        ], toolbar_location="left")

        # pandas_bokeh.save(plot_grid)
        save(plot_grid)


def plot_lines_dashboard_ita(cases_df, figures_path, geo_name, plot_dashboard_flag):
    for save_flag in [False]:
        p1 = plot_df_lines_bokeh(
            cases_df, "data", [
                "totale_tamponi",
                "totale_casi",
            ], figures_path, "tamponi", save_flag
        )

        p2 = plot_df_lines_bokeh(
            cases_df, "data", [
                "totale_attualmente_positivi",
                "totale_deceduti",
                "totale_dimessi_guariti"
            ], figures_path, "totali_principali", save_flag
        )

        p3 = plot_df_lines_bokeh(
            cases_df, "data", [
                "nuovi_positivi",
                "nuovi_attualmente_positivi",
                "nuovi_deceduti",
                "nuovi_dimessi_guariti"
            ], figures_path, "nuovi_principali", save_flag
        )

        p4 = plot_df_lines_bokeh(
            cases_df, "data", [
                "tasso_positivi_tamponi",
                "tasso_nuovi_positivi",
                "tasso_mortalita",
                "tasso_guarigione"
            ], figures_path, "tassi_principali", save_flag
        )

        p5 = plot_df_lines_bokeh(
            cases_df, "data", [
                "attualmente_isolamento_domiciliare",
                "attualmente_ricoverati",
                "attualmente_terapia_intensiva",
            ], figures_path, "dettaglio_pazienti_attuali", save_flag
        )

        p6 = plot_df_lines_bokeh(
            cases_df, "data", [
                "tasso_ricoverati_con_sintomi",
                "tasso_terapia_intensiva",
                "tasso_terapia_intensiva_ricoverati",
            ], figures_path, "tassi_condizioni_cliniche", save_flag
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

        # pandas_bokeh.save(plot_grid)
        save(plot_grid)


def plot_regions_comparison(regions_df, y_col, x_col):
    df_regions_plot = pd.DataFrame(
        index=regions_df[x_col].unique()
    )

    plot = Plot(
        title=None,
        plot_width=1000,
        plot_height=600,
        min_border=0,
        toolbar_location='left'
    )

    colors = itertools.cycle(Dark2_5)

    for region, df_region in regions_df.groupby("denominazione_regione"):
        print(df_region.set_index(x_col)[y_col])

        df_regions_plot.loc[
            df_region.set_index(x_col).index, region
        ] = df_region.set_index(x_col)[y_col].values

        source = ColumnDataSource(
            dict(
                x=df_region.set_index(x_col).index.values,
                y=df_region.set_index(x_col)[y_col].values
            )
        )
        glyph = Line(
            x="x", y="y",
            line_color=next(colors),
            line_width=2,
            line_alpha=0.7,
        )
        plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    curdoc().add_root(plot)
    show(plot)


def get_bokeh_plotter(cases_df, figures_path, geo_name, plot_dashboard_flag, type):
    for save_flag in [False]:

        if type == graph_types[0]:
            p1 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "totale_tamponi",
                    "totale_casi",
                ], figures_path, "tamponi", save_flag
            )
            return p1
        elif type == graph_types[1]:
            p2 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "totale_attualmente_positivi",
                    "totale_deceduti",
                    "totale_dimessi_guariti"
                ], figures_path, "totali_principali", save_flag
            )
            return p2
        elif type == graph_types[2]:
            p3 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "nuovi_positivi",
                    "nuovi_attualmente_positivi",
                    "nuovi_deceduti",
                    "nuovi_dimessi_guariti"
                ], figures_path, "nuovi_principali", save_flag
            )
            return p3
        elif type == graph_types[3]:
            p4 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "tasso_positivi_tamponi",
                    "tasso_nuovi_positivi",
                    "tasso_mortalita",
                    "tasso_guarigione"
                ], figures_path, "tassi_principali", save_flag
            )
            return p4
        elif type == graph_types[4]:

            p5 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "attualmente_isolamento_domiciliare",
                    "attualmente_ricoverati",
                    "attualmente_terapia_intensiva",
                ], figures_path, "dettaglio_pazienti_attuali", save_flag
            )
            return p5
        elif type == graph_types[5]:
            p6 = plot_df_lines_bokeh(
                cases_df, "data", [
                    "tasso_ricoverati_con_sintomi",
                    "tasso_terapia_intensiva",
                    "tasso_terapia_intensiva_ricoverati",
                ], figures_path, "tassi_condizioni_cliniche", save_flag
            )
            return p6
