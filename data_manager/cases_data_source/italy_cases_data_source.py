import os

import pandas as pd

from data_manager.config.config import raw_cases_paths_dict
from data_manager.config.config import norm_cases_paths


class ItalyCasesDataSource:

	def __init__(self):

		self.raw_cases_country_df = pd.read_csv(
			os.path.join(
				raw_cases_paths_dict["italy"],
				"dati-andamento-nazionale",
				"dpc-covid19-ita-andamento-nazionale.csv"
			)
		).drop(["note_it", "note_en"], axis=1).dropna()

		self.norm_data_path = os.path.join(
			norm_cases_paths,
			"italy"
		)
		os.makedirs(self.norm_data_path, exist_ok=True)

		self.raw_cases_regions_df = pd.read_csv(
			os.path.join(
				raw_cases_paths_dict["italy"],
				"dati-regioni",
				"dpc-covid19-ita-regioni.csv"
			)
		).drop(["note_it", "note_en"], axis=1).dropna()

		self.norm_country_df_ita = pd.DataFrame()
		self.norm_country_df = pd.DataFrame()

	def normalise(self):

		self.norm_country_df_ita = self.raw_cases_country_df.copy()
		self.norm_country_df_ita["nuovi_deceduti"] = self.norm_country_df_ita.deceduti.diff()
		self.norm_country_df_ita["nuovi_dimessi_guariti"] = self.norm_country_df_ita.dimessi_guariti.diff()
		self.norm_country_df_ita["nuovi_positivi_conclusi"] = \
			self.norm_country_df_ita.nuovi_deceduti + self.norm_country_df_ita.nuovi_dimessi_guariti
		self.norm_country_df_ita["totale_positivi_conclusi"] = \
			self.norm_country_df_ita.deceduti + self.norm_country_df_ita.dimessi_guariti
		self.norm_country_df_ita["nuovi_positivi_totali"] = \
			self.norm_country_df_ita.nuovi_attualmente_positivi + self.norm_country_df_ita.nuovi_positivi_conclusi
		self.norm_country_df_ita["totale_casi_attivi"] = \
			self.norm_country_df_ita.totale_casi - self.norm_country_df_ita.totale_positivi_conclusi

		self.norm_country_df = self.raw_cases_country_df.rename({
			"data": "datetime",
			"ricoverati_con_sintomi": "currently_hospitalised",
			"terapia_intensiva": "currently_intensive_care",
			"totale_ospedalizzati": "total_currently_hospitalised",
			"isolamento_domiciliare": "currently_home_isolation",
			"totale_attualmente_positivi": "total_currently_positives",
			"nuovi_attualmente_positivi": "new_currently_positives",
			"dimessi_guariti": "total_recovered",
			"deceduti": "total_deaths",
			"tamponi": "total_tests",
		}, axis=1)
		self.norm_country_df["total_concluded_cases"] = \
			self.norm_country_df.total_deaths + self.norm_country_df.total_recovered
		self.norm_country_df["new_deaths"] = self.norm_country_df.total_deaths.diff()
		self.norm_country_df["new_recovered"] = self.norm_country_df.total_recovered.diff()
		self.norm_country_df["new_concluded_cases"] = \
			self.norm_country_df.new_deaths + self.norm_country_df.new_recovered
		self.norm_country_df["new_total_positives"] = \
			self.norm_country_df.new_currently_positives + self.norm_country_df.new_concluded_cases

	def save_norm(self):

		self.norm_country_df.to_csv(
			os.path.join(
				self.norm_data_path,
				"country_df.csv"
			)
		)
		self.norm_country_df_ita.to_csv(
			os.path.join(
				self.norm_data_path,
				"country_df_ita.csv"
			)
		)

	def load_norm(self):
		data_path = os.path.join(
			os.path.join(
				self.norm_data_path,
				"country_df.csv"
			)
		)
		self.norm_country_df = pd.read_csv(data_path, index_col=0)
		data_path = os.path.join(
			os.path.join(
				self.norm_data_path,
				"country_df_ita.csv"
			)
		)
		self.norm_country_df_ita = pd.read_csv(data_path, index_col=0)
		return self.norm_country_df_ita
