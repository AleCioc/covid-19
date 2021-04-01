import streamlit as st

from covid_19.dashboard_field.dashboard_field import DashboardField
from functools import partial

class DashboardMain(DashboardField):

    def __init__(self, title, available_fields, subtitle = "", logo=""):
        wl = [partial(st.sidebar.selectbox, "Scegli quale schermata visualizzare", self.get_screen_names(available_fields))]
        super().__init__(widget_location=st.sidebar, title=title, name="Schermata principale", subtitle=subtitle, widget_list=wl)
        self.available_screens_list = available_fields
        self.logo = logo



    def show_configuration(self):
        self.widget_location.image(self.logo)
        self.location.markdown("# "+self.title)



    def get_screen_names(self, list):
        ret = []
        if len(list)==0:
            return ret
        for screen in list:
            ret.append(screen.get_name())
        return ret

    def show_screen(self, screen_name):
        for screen in self.available_screens_list:
            if screen.get_name() == screen_name:
                screen.show_configuration()
                screen.show_charts()
                break
