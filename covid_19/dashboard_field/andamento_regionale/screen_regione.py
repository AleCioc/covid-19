from covid_19.dashboard_field import ChartStandard
from covid_19.dashboard_field.andamento_regionale.char_bar import ChartBar
from covid_19.dashboard_field.andamento_regionale.chart_slider import ChartSlider
from covid_19.dashboard_field.confronto_regioni.chart_pie import ChartPie
from covid_19.dashboard_field.dashboard_report import DashboardReport
from covid_19.dashboard_field.dashboard_screen import DashboardScreen
from covid_19.dashboard_field.utils import regioni, transform_region_to_pc, transform_regions_pc_to_human, transform_regions_pc_to_human_all
from covid_19.dashboard_field.utils import NUMERO_GRAFICI, graph_types, graph_subtitles, graph_titles, get_norm_data, articoli_regioni_no_in, determina_scelte, st_functional_columns
import streamlit as st
import datetime
from functools import partial
import os

from covid_19.data_manager import raw_cases_paths_dict


class ScreenRegione(DashboardScreen):

    def __init__(self, title, name, chart_list=None, subtitle=""):
        super().__init__(title, name, chart_list=None, subtitle=subtitle)
        # la chart_list me la creo io man mano, cosi non devo memorizzare grafici inutili
        self.chart_dict = {}

        self.data = get_norm_data()


    def show_widgets(self, location=None):

        col1, col2 = st.beta_columns(2)
        regione = transform_region_to_pc(col1.selectbox("Di quale regione vuoi visualizzare i dati?", transform_regions_pc_to_human_all()))
        type = col2.selectbox("Quale libreria di plotting vuoi utilizzare per i grafici?", ["Altair", "Bokeh", "Pyplot"])

        return regione, type

    def show_charts(self):

        #controllo se ho i dati aggiornati. Se sono aggiornati bene, altrimenti scarica i nuovi
        self.data = get_norm_data()

        regione, tipo = self.show_widgets()

        #report
        DashboardReport("Report", self.get_last_day(self.data, regione), regione).show()

        #grafici classici
        giorno = len(os.listdir(os.path.join(raw_cases_paths_dict["italy"], "dati-andamento-nazionale")))

        if giorno not in self.chart_dict:
            self.chart_dict = {}
            self.chart_dict[giorno] = {}

        if tipo in self.chart_dict[giorno] and regione in self.chart_dict[giorno][tipo]:
            for i in range(NUMERO_GRAFICI):
                self.chart_dict[giorno][tipo][regione][i].show()
        else:
            if tipo not in self.chart_dict[giorno]:
                self.chart_dict[giorno][tipo] = {}
            self.chart_dict[giorno][tipo][regione] = []

            for i in range(NUMERO_GRAFICI):
                articolo = "in"
                if regione in articoli_regioni_no_in:
                    articolo = articoli_regioni_no_in[regione]

                titolo = graph_titles[i]+" "+articolo+" "+transform_regions_pc_to_human(regione)
                self.chart_dict[giorno][tipo][regione].append((ChartStandard(self.data, graph_types[i], title=titolo,
                                                               subtitle=graph_subtitles[i], regione=regione, tipo=tipo)))

            for i in range(NUMERO_GRAFICI):
                self.chart_dict[giorno][tipo][regione][i].show()

        #Grafico extra 1

        # creo il report per il periodo personalizzato
        titolo = "Periodo personalizzato"
        sub = "In questo grafico è possibile visualizzare l'andamento di un parametro a scelta della regione analizzata in un intervallo temporale a scelta."

        min = datetime.datetime.fromisoformat(str(self.data.norm_regions_df_ita.data.min()))
        max = datetime.datetime.fromisoformat(str(self.data.norm_regions_df_ita.data.max()))

        args = [["slider", "Di che periodo?", min, max, (min, max)], [],
                        ["selectbox", "Quale parametro?", determina_scelte(self.data.norm_regions_df_ita)]]
        wl = [partial(st_functional_columns, args, (0.6, 0.1, 0.3))]

        ChartSlider(name=titolo, title=titolo, subtitle=sub, widget_list=wl, dati=get_norm_data(), regione=regione, tipo=tipo).show()

        # creo il barchart
        titolo = "Andamento mensile "
        if regione not in articoli_regioni_no_in:
            titolo+="in"
        else:
            titolo+=articoli_regioni_no_in[regione]
        titolo+=" "+transform_regions_pc_to_human(regione)
        sub = "In questo grafico è possibile visualizzare l'andamento di un parametro a scelta della regione analizzata in un mese prefissato."

        mesi_disponibili = [
            (3, 2020), (4, 2020), (5, 2020), (6, 2020), (7, 2020), (8, 2020), (9, 2020), (10, 2020),
            (11, 2020), (12, 2020), (1, 2021), (2, 2021), (3, 2021)
        ]

        args = [ ["selectbox", "A quale mese sei interessato?", mesi_disponibili], ["selectbox", "Quale parametro vuoi analizzare?", determina_scelte(self.data.norm_regions_df_ita)]]
        wl = [partial(st_functional_columns, args)]

        ChartBar(name=titolo, title=titolo, subtitle=sub, widget_list=wl, dati=get_norm_data(), regione=regione, tipo=tipo).show()

    def get_last_day(self, data, regione):
        df = data.norm_regions_df_ita.loc[ data.norm_regions_df_ita.denominazione_regione == regione]
        return df.iloc[-1]

