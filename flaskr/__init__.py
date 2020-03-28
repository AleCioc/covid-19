import os

from threading import Thread
from time import sleep

from flask import Flask, render_template

from data_manager import root_figures_path
from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource
from data_manager.plotter.bokeh_plotter import plot_lines_dashboard_ita


class Bk_worker(Thread):
    def run(self):
        while True:
            italy_cases_ds = ItalyCasesDataSource()
            italy_cases_ds.normalise()
            italy_cases_ds.save_norm()
            country_df = italy_cases_ds.norm_country_df_ita
            # country_df = italy_cases_ds.load_norm()
            regions_df = italy_cases_ds.norm_regions_df_ita

            plot_lines_dashboard_ita(country_df, root_figures_path, "dashboard_italia")
            for region, df_region in regions_df.groupby("denominazione_regione"):
                plot_lines_dashboard_ita(df_region, root_figures_path, "dashboard_" + region)
                break
            sleep(1000)


def create_app():
    # create and configure the app
    app = Flask(__name__, static_url_path="/static")

    #Bk_worker().start()

    # a simple page that says hello
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route('/dash/<zone>')
    def dash(zone):
        return app.send_static_file("dashboard_" + zone + ".html")

    return app
