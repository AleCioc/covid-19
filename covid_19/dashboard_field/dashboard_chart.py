from covid_19.dashboard_field.dashboard_field import DashboardField
import streamlit as st


class DashboardChart(DashboardField):

    def __init__(self, title, name, subtitle=""):
        super().__init__(title, location=st, widget_location=st, name=name, subtitle=subtitle)

    def show_configuration(self):
        self.location.markdown("### **" + self.title+"**")
        self.location.markdown("*" +self.subtitle+"*")

    def show(self):
        """

        :return:
        """
