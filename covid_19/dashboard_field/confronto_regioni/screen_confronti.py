from functools import partial

from covid_19.dashboard_field.confronto_regioni.chart_interattivo import ChartInterattivo
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import get_norm_data, transform_regions_pc_to_human_all, determina_scelte, st_functional_columns

class ScreenConfronti(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=None, widget_list = None):
        super().__init__(title,name,chart_list,subtitle, widget_list)
        self.chart_dict = {}
        self.data = get_norm_data()

    def show_charts(self):

        name = "Andamento temporale e massimi"
        subtitle = "In questo grafico interattivo puoi selezionare il periodo (direttamente sul grafico), le regioni e il parametro (dai widget)"
        arg = [["multiselect", "Seleziona la regione", transform_regions_pc_to_human_all()],
               ["selectbox", "Quale parametro vuoi confrontare?", determina_scelte(self.data.norm_regions_df_ita)]]
        wl = [ partial(st_functional_columns, arg)]
        ChartInterattivo(name, name, subtitle, self.data, widget_list=wl).show()