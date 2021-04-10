import streamlit as st

from covid_19.dashboard_field.dashboard_field import DashboardField
from functools import partial

class DashboardMain(DashboardField):

    def __init__(self, title, available_fields, subtitle = "", logo=""):
        self.available_screens_list = available_fields
        wl = [partial(st.sidebar.selectbox, "Scegli quale schermata visualizzare", self.get_screen_names())]
        super().__init__(widget_location=st.sidebar, title=title, name="Schermata principale", subtitle=subtitle, widget_list=wl)
        self.logo = logo



    def show_heading(self):
        self.widget_location.image(self.logo)
        self.location.markdown("# "+self.title)



    def get_screen_names(self):
        list = self.available_screens_list
        ret = []
        if len(list)==0:
            return ret
        for screen in list:
            ret.append(screen.get_name())
        return ret

    def show_screen(self, screen_name):
        for screen in self.available_screens_list:
            if screen.get_name() == screen_name:
                screen.show_heading()
                screen.show_charts()
                break

    def show(self):
        self.show_heading()
        scelto = self.show_widgets()[0]
        self.show_screen(scelto)