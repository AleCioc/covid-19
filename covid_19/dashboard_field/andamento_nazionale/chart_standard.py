from covid_19.dashboard_field.dashboard_chart import DashboardChart


class ChartStandard(DashboardChart):

    def __init__(self, data, parametro, title, subtitle, regione):
        super().__init__(title, name=title, subtitle=subtitle)
        self.data = data
        self.parametro=parametro
        self.regione = regione


    def show(self):
        self.show_configuration()
        self.data.plot_dashboard_st(type=self.parametro, regione=self.regione, show_also_bokeh=False)