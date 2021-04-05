import os

from covid_19.dashboard_field.andamento_nazionale.chart_standard import ChartStandard
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import get_norm_data, graph_types, graph_titles, graph_subtitles
from covid_19.data_manager import raw_cases_paths_dict


class ScreenNazione(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=None, widget_list = None, stato="Italia"):
        super().__init__(title,name,chart_list,subtitle, widget_list)
        self.chart_dict = {}
        self.data = get_norm_data()
        self.stato = stato

    def show_charts(self):
        tipo = self.show_widgets()[0]
        giorno = len(os.listdir(os.path.join(raw_cases_paths_dict["italy"],"dati-andamento-nazionale")))

        if giorno not in self.chart_dict:
            self.chart_dict = {}
            self.chart_dict[giorno] = {}

        if tipo not in self.chart_dict[giorno]:
            self.chart_dict[giorno][tipo] = []
            for i in range(len(graph_types)):
                self.chart_dict[giorno][tipo].append(ChartStandard(self.data, graph_types[i], title=graph_titles[i]+" in "+self.stato, subtitle=graph_subtitles[i],
                                         regione="italia",tipo=tipo))
            for i in range(len(graph_types)):
                self.chart_dict[giorno][tipo][i].show()
        else:
            for i in range(len(graph_types)):
                self.chart_dict[giorno][tipo][i].show()
