import streamlit as st


class DashboardField():

    def __init__(self, title="", location=st, widget_location=st, name="", subtitle=""):
        self.title = title
        self.location = location
        self.widget_location = widget_location
        self.name = name
        self.subtitle = subtitle

    def show_configuration(self):
        """
        Mostra titolo e eventuale sottotitolo. I titoli sono i markdown con il numero di # che dipende dall'importanza
        :return:
        """

    def show_widgets(self):
        """
        Da implementare, mostra i widget nella posizione self.widget_location
        :return: i valori letti dai widget
        """

    def get_name(self):
        return self.name