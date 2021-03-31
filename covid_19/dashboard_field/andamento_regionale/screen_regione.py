from covid_19.dashboard_field import ChartStandard
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import regioni, transform_region_to_pc, transform_regions_pc_to_human, transform_regions_pc_to_human_all
from covid_19.dashboard_field.utils import NUMERO_GRAFICI, graph_types, graph_subtitles, graph_titles, get_norm_data, articoli_regioni_no_in


class ScreenRegione(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=""):
        super().__init__(title, name, chart_list=None, subtitle=subtitle)
        # la chart_list me la creo io man mano, cosi non devo memorizzare grafici inutili
        self.chart_dict = {}
        self.data = get_norm_data()

    def show_widgets(self):
        return transform_region_to_pc(self.widget_location.selectbox("Di quale regione vuoi visualizzare i dati?", transform_regions_pc_to_human_all()))

    def show_charts(self):

        regione = self.show_widgets()

        if regione in self.chart_dict:
            for i in range(NUMERO_GRAFICI):
                self.chart_dict[regione][i].show()
        else:
            self.chart_dict[regione] = []

            for i in range(NUMERO_GRAFICI):
                articolo = "in"
                if regione in articoli_regioni_no_in:
                    articolo = articoli_regioni_no_in[regione]

                titolo = graph_titles[i]+" "+articolo+" "+transform_regions_pc_to_human(regione)
                self.chart_dict[regione].append((ChartStandard(self.data, graph_types[i], title=titolo,
                                                               subtitle=graph_subtitles[i], regione=regione)))

            for i in range(NUMERO_GRAFICI):
                self.chart_dict[regione][i].show()
