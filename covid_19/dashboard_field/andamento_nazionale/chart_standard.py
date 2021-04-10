from covid_19.dashboard_field.dashboard_chart import DashboardChart


class ChartStandard(DashboardChart):

    def __init__(self, data, parametro, title, subtitle, regione, tipo="Altair"):
        super().__init__(title, name=title, subtitle=subtitle)
        self.data = data
        self.parametro=parametro
        self.regione = regione
        self.tipo = tipo


    def show(self):
        self.show_heading()
        self.data.plot_dashboard_st(type=self.parametro, regione=self.regione, tipo=self.tipo)