from __future__ import print_function
import json

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers
from threading import Thread
from time import sleep
from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from data_manager.config.config import *

from data_manager.plotter.bokeh_plotter import *

from flask import Flask, render_template

from data_manager import root_figures_path
from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource
from data_manager.plotter.bokeh_plotter import plot_lines_dashboard_ita

from flask import Flask
from jinja2 import Template

app = Flask(__name__)

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]


@app.route("/")
def index():
    page = Template(open("templates\\index.html", "r").read())
    return page.render(resources=CDN.render())


@app.route('/<country>/<region>/<type>')
def dash(country, region, type):
    with open('static\\' + country + '\\' + region + '\\' + type + '.json') as json_file:
        return json.load(json_file)

@app.route('/dash_options')
def dash_options():
    with open("static\\options.json") as file:
        return json.load(file)


class Bk_worker(Thread):
    def run(self):
        def dash_options(path):
            data = {}
            walk = os.walk(path)
            root, states, files = walk.__next__()
            for state in states:
                root, regions, files = walk.__next__()
                data[state] = {}
                for region in regions:
                    data[state][region] = []
                    root, dirs, files = walk.__next__()
                    for file in files:
                        if os.path.splitext(file)[1] == '.json':
                            data[state][region].append(os.path.splitext(file)[0])
            return data

        while True:
            italy_cases_ds = ItalyCasesDataSource()
            italy_cases_ds.normalise()
            # italy_cases_ds.save_norm()
            # country_df = italy_cases_ds.load_norm()

            country_df = italy_cases_ds.norm_country_df_ita.set_index("data")
            regions_df = italy_cases_ds.norm_regions_df_ita.set_index("data")
            country_df["datetime"] = country_df.index.values
            country_df["data"] = country_df["datetime"].apply(lambda d: str(d.date()))

            country_path = os.path.join(
                italy_figures_path,
                "country"
            )
            os.makedirs(country_path, exist_ok=True)
            plot_lines_dashboard_ita(country_df, country_path)
            for region, df_region in regions_df.groupby("denominazione_regione"):
                print(region)
                region_path = os.path.join(
                    italy_figures_path,
                    region
                )
                os.makedirs(region_path, exist_ok=True)
                plot_lines_dashboard_ita(df_region, region_path)
            json.dump(dash_options("static"), open("static\\options.json", "w"))
            sleep(1000)




if __name__ == '__main__':
    #Bk_worker().start()

    app.run(host='0.0.0.0')
