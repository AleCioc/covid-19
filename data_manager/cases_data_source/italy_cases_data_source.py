import os
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

from data_manager.config.config import *
from data_manager.plotter.bokeh_plotter import *
from data_manager.plotter.cases_plotter import ItalyCasesPlotter

cols = [
	'data',
	'stato',
	'codice_regione',
	'denominazione_regione',
	'lat',
	'long',
	'ricoverati_con_sintomi',
	'terapia_intensiva',
	'totale_ospedalizzati',
	'isolamento_domiciliare',
	'totale_attualmente_positivi',
	'nuovi_attualmente_positivi',
	'dimessi_guariti',
	'deceduti',
	'totale_casi',
	'tamponi'
]


def rename_columns_ita(ita_df):
	return ita_df.rename({
		"totale_positivi": "totale_attualmente_positivi",
		"variazione_totale_positivi": "nuovi_attualmente_positivi",
		"ricoverati_con_sintomi": "attualmente_ricoverati",
		"terapia_intensiva": "attualmente_terapia_intensiva",
		"totale_ospedalizzati": "attualmente_ospedalizzati",
		"isolamento_domiciliare": "attualmente_isolamento_domiciliare",
		"dimessi_guariti": "totale_dimessi_guariti",
		"deceduti": "totale_deceduti",
		"tamponi": "totale_tamponi",
	}, axis=1)


def translate_columns_ita_to_eng(ita_df):
	return ita_df.rename({
		"data": "datetime",
		"codice_regione": "region_id",
		"denominazione_regione": "region_name",
		"ricoverati_con_sintomi": "currently_hospitalised",
		"terapia_intensiva": "currently_intensive_care",
		"totale_ospedalizzati": "total_currently_hospitalised",
		"isolamento_domiciliare": "currently_home_isolation",
		"totale_attualmente_positivi": "total_currently_positives",
		"nuovi_attualmente_positivi": "new_currently_positives",
		"dimessi_guariti": "total_recovered",
		"deceduti": "total_deaths",
		"tamponi": "total_tests",
		"totale_casi": "total_cases",
	}, axis=1)


def add_missing_features_ita(cases_df_ita):

	day_threshold_cases = cases_df_ita[
		cases_df_ita.totale_casi > 100
	].data.min()

	cases_df_ita["day_threshold_cases"] = (
			cases_df_ita.data.apply(lambda d: d.date()) - day_threshold_cases.date()
	).apply(lambda td: td.days)

	cases_df_ita["totale_positivi_conclusi"] = cases_df_ita.totale_deceduti + cases_df_ita.totale_dimessi_guariti
	cases_df_ita["nuovi_deceduti"] = cases_df_ita.totale_deceduti.diff()
	cases_df_ita["nuovi_dimessi_guariti"] = cases_df_ita.totale_dimessi_guariti.diff()
	cases_df_ita["nuovi_positivi_conclusi"] = cases_df_ita.nuovi_deceduti + cases_df_ita.nuovi_dimessi_guariti
	cases_df_ita["nuovi_positivi"] = cases_df_ita.nuovi_attualmente_positivi + cases_df_ita.nuovi_positivi_conclusi

	cases_df_ita["tasso_positivi_tamponi"] = cases_df_ita['totale_casi'] / cases_df_ita['totale_tamponi']
	cases_df_ita["tasso_nuovi_positivi"] = cases_df_ita['nuovi_positivi'] / cases_df_ita['totale_casi']
	cases_df_ita["tasso_mortalita"] = cases_df_ita['totale_deceduti'] / cases_df_ita['totale_casi']
	cases_df_ita["tasso_guarigione"] = cases_df_ita['totale_dimessi_guariti'] / cases_df_ita['totale_casi']

	cases_df_ita["tasso_ricoverati_con_sintomi"] = (
			cases_df_ita['attualmente_ricoverati'] / cases_df_ita['totale_attualmente_positivi']
	)
	cases_df_ita["tasso_terapia_intensiva"] = (
			cases_df_ita['attualmente_terapia_intensiva'] / cases_df_ita['totale_attualmente_positivi']
	)
	cases_df_ita["tasso_terapia_intensiva_ricoverati"] = (
			cases_df_ita['attualmente_terapia_intensiva'] / cases_df_ita['attualmente_ricoverati']
	)

	return cases_df_ita


def add_missing_features_eng(cases_df):
	cases_df["new_deaths"] = cases_df.total_deaths.diff()
	cases_df["new_recovered"] = cases_df.total_recovered.diff()
	cases_df["new_concluded_cases"] = cases_df.new_deaths + cases_df.new_recovered
	cases_df["new_positives"] = cases_df.total_cases.diff()
	cases_df["total_concluded_cases"] = cases_df.total_deaths + cases_df.total_recovered
	cases_df["new_currently_positives"] = (cases_df.total_cases - cases_df.total_concluded_cases).diff()
	cases_df["rate_new_positives"] = cases_df['new_positives'] / cases_df['total_cases']
	cases_df["rate_deaths"] = cases_df['total_deaths'] / cases_df['total_cases']
	cases_df["rate_recovered"] = cases_df['total_recovered'] / cases_df['total_cases']
	return cases_df


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

		self.raw_cases_country_df["data"] = pd.to_datetime(self.raw_cases_country_df["data"], utc=True)
		self.raw_cases_regions_df["data"] = pd.to_datetime(self.raw_cases_regions_df["data"], utc=True)
		self.raw_cases_regions_df["denominazione_regione"] = self.raw_cases_regions_df["denominazione_regione"].apply(
			lambda s: s.replace(" ", "").replace(".", "").replace("'", "").lower()
		)
		#print(self.raw_cases_country_df.columns)

		self.norm_country_df_ita = pd.DataFrame()
		self.norm_country_df = pd.DataFrame()

		self.norm_regions_df_ita = pd.DataFrame()
		self.norm_regions_df = pd.DataFrame()

	def normalise(self):

		self.norm_country_df_ita = self.raw_cases_country_df.copy()
		self.norm_country_df = translate_columns_ita_to_eng(self.norm_country_df_ita)
		self.norm_country_df = add_missing_features_eng(self.norm_country_df)
		self.norm_country_df_ita = rename_columns_ita(self.norm_country_df_ita)
		self.norm_country_df_ita = add_missing_features_ita(self.norm_country_df_ita)

		self.norm_regions_df_ita = self.raw_cases_regions_df.copy()
		self.norm_regions_df = translate_columns_ita_to_eng(self.norm_regions_df_ita)
		self.norm_regions_df_ita = rename_columns_ita(self.norm_regions_df_ita)

		for region, df_region in self.norm_regions_df.groupby("region_id"):
			df_region = add_missing_features_eng(
				df_region.fillna(0)
			)
			for col in df_region:
				self.norm_regions_df.loc[df_region.index, col] = df_region[col].copy()

		for region, df_region in self.norm_regions_df_ita.groupby("codice_regione"):
			df_region = add_missing_features_ita(
				df_region.fillna(0)
			)
			df_region = rename_columns_ita(df_region)
			for col in df_region:
				self.norm_regions_df_ita.loc[df_region.index, col] = df_region[col].copy()

	def plot_dashboard (self):

		plotter = ItalyCasesPlotter(
			self.norm_country_df_ita,
			self.norm_regions_df_ita
		)
		plotter.plot_dashboard_ita(True, True)

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

		self.norm_regions_df_ita.to_csv(
			os.path.join(
				self.norm_data_path,
				"regions_df.csv"
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
