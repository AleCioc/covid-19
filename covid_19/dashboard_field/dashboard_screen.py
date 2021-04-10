from covid_19.dashboard_field.dashboard_field import DashboardField
import streamlit as st

class DashboardScreen(DashboardField):

    def __init__(self, title, name, chart_list=None, subtitle="", widget_list=None):
        super().__init__(title=title, widget_location=st, name=name, subtitle=subtitle, widget_list=widget_list)
        if chart_list is None:
            chart_list = []
        self.chart_list = chart_list

    def show_heading(self):
        self.location.markdown("## "+self.title)
        self.location.write(self.subtitle)

    def show_charts(self):
        for chart in self.chart_list:
            chart.show()



