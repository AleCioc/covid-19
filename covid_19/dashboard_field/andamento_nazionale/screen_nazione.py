from covid_19.dashboard_field.andamento_nazionale.chart_standard import ChartStandard
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import get_norm_data, graph_types, graph_titles, graph_subtitles

class ScreenNazione(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=None, widget_list = None, stato="Italia"):
        super().__init__(title,name,chart_list,subtitle, widget_list)
        self.chart_dict = {}
        self.data = get_norm_data()
        self.stato = stato

    def show_charts(self):
        tipo = self.show_widgets()[0]

        if tipo not in self.chart_dict:
            self.chart_dict[tipo] = []
            for i in range(len(graph_types)):
                self.chart_dict[tipo].append(ChartStandard(self.data, graph_types[i], title=graph_titles[i]+" in "+self.stato, subtitle=graph_subtitles[i],
                                         regione="italia",tipo=tipo))
            for i in range(len(graph_types)):
                self.chart_dict[tipo][i].show()
        else:
            for i in range(len(graph_types)):
                self.chart_dict[tipo][i].show()
