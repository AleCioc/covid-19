from covid_19.dashboard_field import ChartStandard
from covid_19.dashboard_field.andamento_regionale.chart_slider import ChartSlider
from covid_19.dashboard_field.dashboard_report import DashboardReport
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import regioni, transform_region_to_pc, transform_regions_pc_to_human, transform_regions_pc_to_human_all
from covid_19.dashboard_field.utils import NUMERO_GRAFICI, graph_types, graph_subtitles, graph_titles, get_norm_data, articoli_regioni_no_in, determina_scelte
import streamlit as st
import datetime
from functools import partial

class ScreenRegione(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=""):
        super().__init__(title, name, chart_list=None, subtitle=subtitle)
        # la chart_list me la creo io man mano, cosi non devo memorizzare grafici inutili
        self.chart_dict = {}
        self.data = get_norm_data()


    def show_widgets(self, location=None):

        col1, col2 = st.beta_columns(2)
        regione = transform_region_to_pc(col1.selectbox("Di quale regione vuoi visualizzare i dati?", transform_regions_pc_to_human_all()))
        type = col2.selectbox("Quale libreria di plotting vuoi utilizzare per i grafici?", ["Altair", "Bokeh", "Plotly"])

        return regione, type

    def show_charts(self):

        regione, tipo = self.show_widgets()


        if tipo in self.chart_dict and regione in self.chart_dict[tipo]:
            self.chart_dict[tipo][regione][NUMERO_GRAFICI].show()
            for i in range(NUMERO_GRAFICI):
                self.chart_dict[tipo][regione][i].show()
            self.chart_dict[tipo][regione][NUMERO_GRAFICI+ 1].show()
        else:
            if tipo not in self.chart_dict:
                self.chart_dict[tipo] = {}
            self.chart_dict[tipo][regione] = []

            for i in range(NUMERO_GRAFICI):
                articolo = "in"
                if regione in articoli_regioni_no_in:
                    articolo = articoli_regioni_no_in[regione]

                titolo = graph_titles[i]+" "+articolo+" "+transform_regions_pc_to_human(regione)
                self.chart_dict[tipo][regione].append((ChartStandard(self.data, graph_types[i], title=titolo,
                                                               subtitle=graph_subtitles[i], regione=regione, tipo=tipo)))
            #creo il report

            self.chart_dict[tipo][regione].append(DashboardReport("Report", self.get_last_day(self.data, regione), regione))

            #creo il report per il periodo personalizzato
            titolo = "Periodo personalizzato"
            sub = "In questo grafico è possibile visualizzare l'andamento di un parametro a scelta della regione analizzata in un intervallo temporale a scelta."

            min = datetime.datetime.fromisoformat(str(self.data.norm_regions_df_ita.data.min()))
            max = datetime.datetime.fromisoformat(str(self.data.norm_regions_df_ita.data.max()))

            wl = [ partial(st.slider, "Di che periodo?", min_value=min, max_value=max, value=(min, max)),
                   partial(st.selectbox, "Quale parametro?", determina_scelte(self.data.norm_regions_df_ita))
                   ]
            self.chart_dict[tipo][regione].append(ChartSlider(name=titolo, title = titolo, subtitle=sub, widget_list=wl, dati = get_norm_data(), regione = regione))

            self.chart_dict[tipo][regione][NUMERO_GRAFICI].show()

            for i in range(NUMERO_GRAFICI):
                self.chart_dict[tipo][regione][i].show()
            self.chart_dict[tipo][regione][NUMERO_GRAFICI+1].show()

    def get_last_day(self, data, regione):
        df = data.norm_regions_df_ita.loc[ data.norm_regions_df_ita.denominazione_regione == regione]
        return df.iloc[-1]

