import streamlit as st


class DashboardField():

    def __init__(self, title="", location=st, widget_location=st, name="", subtitle="", widget_list=None):
        if widget_list is None:
            widget_list = []
        self.title = title
        self.location = location
        self.widget_location = widget_location
        self.name = name
        self.subtitle = subtitle
        self.widget_list = widget_list

    def show_configuration(self):
        """
        Mostra titolo e eventuale sottotitolo. I titoli sono i markdown con il numero di # che dipende dall'importanza
        :return:
        """

    def show_widgets(self):
        ret = []
        for widget in self.widget_list:
            r = widget()
            print(r)
            ret.append(r)
        return tuple(ret)


    def get_name(self):
        return self.name