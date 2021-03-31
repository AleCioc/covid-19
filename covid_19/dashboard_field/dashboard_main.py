import streamlit as st

from covid_19.dashboard_field.dashboard_field import DashboardField


class DashboardMain(DashboardField):

    def __init__(self, title, available_fields, subtitle = "", logo=""):
        super().__init__(widget_location=st.sidebar, title=title, name="Schermata principale", subtitle=subtitle)
        self.available_screens_list = available_fields
        self.logo = logo

    def show_widgets(self):
        field_names = self.get_screen_names(self.available_screens_list)
        return self.widget_location.selectbox("Scegli quale schermata visualizzare", field_names)


    def show_configuration(self):
        self.widget_location.image(self.logo)
        self.location.markdown("# "+self.title)



    def get_screen_names(self, list):
        ret = []
        if len(self.available_screens_list)==0:
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
