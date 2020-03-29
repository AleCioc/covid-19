import os
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

from data_manager.config.config import *
from data_manager.plotter.bokeh_plotter import *


def read_raw_data():

	confirmed_df = pd.read_csv(
		os.path.join(
			raw_cases_paths_dict["world"],
			"csse_covid_19_data",
			"csse_covid_19_time_series",
			"time_series_covid19_confirmed_global.csv",
		)
	)
	deaths_df = pd.read_csv(
		os.path.join(
			raw_cases_paths_dict["world"],
			"csse_covid_19_data",
			"csse_covid_19_time_series",
			"time_series_covid19_deaths_global.csv",
		)
	)
	recovered_df = pd.read_csv(
		os.path.join(
			raw_cases_paths_dict["world"],
			"csse_covid_19_data",
			"csse_covid_19_time_series",
			"time_series_covid19_recovered_global.csv",
		)
	)

	def preprocess(df, col_name):

		raw_world_df = pd.DataFrame()
		datetime_index = df.iloc[:, 4:].T.index
		datetime_series = pd.Series(datetime_index.values)
		df["Province/State"] = df["Province/State"].fillna("mainland")
		for country, country_df in df.groupby("Country/Region"):
			country_categorial_cols = country_df.iloc[:, :4].columns
			country_time_series = country_df.iloc[:, 4:].T.iloc[:, :1]
			country_time_series[col_name] = country_time_series.iloc[:, 0]
			country_time_series["Date"] = country_time_series.index
			country_time_series["Country/Region"] = country
			#print(country_time_series)

			for region, region_df in country_df.groupby("Province/State"):
				country_categorial_cols = country_df.iloc[:, :4].columns
				region_time_series = region_df.iloc[:, 4:].T.iloc[:, :1]
				region_time_series[col_name] = region_time_series.iloc[:, 0]
				region_time_series["Date"] = region_time_series.index
				region_time_series["Province/State"] = region
				for col in country_categorial_cols:
					region_time_series[col] = region_df[col].unique()[0]
				#print(region_time_series)
				raw_world_df = pd.concat([
					raw_world_df,
					region_time_series.iloc[:, 1:]
				], axis=0, ignore_index=True)

			#print(raw_world_df)

		return raw_world_df

	raw_world_df = preprocess(confirmed_df, "Confirmed")
	raw_world_df["Deaths"] = preprocess(deaths_df, "Deaths")["Deaths"]
	raw_world_df["Recovered"] = preprocess(recovered_df, "Recovered")["Recovered"]

	return raw_world_df


def rename_columns(world_df):
	return world_df.rename({
		"Date": "datetime",
		"Province/State": "region_id",
		"Country/Region": "country_id",
		"Deaths": "total_deaths",
		"Confirmed": "total_cases",
		"Recovered": "total_recovered",
	}, axis=1)


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


class WorldCasesDataSource:

	def __init__(self):

		self.raw_cases_world_df = read_raw_data()

		self.norm_data_path = os.path.join(
			norm_cases_paths,
			"world"
		)
		os.makedirs(self.norm_data_path, exist_ok=True)

		self.norm_world_df = pd.DataFrame()
		self.countries_with_regions = []
		self.countries_without_regions = []
		self.countries_df_dict = {}
		self.countries_with_regions_df_dict = {}

	def normalise(self):

		self.norm_world_df = self.raw_cases_world_df.copy()
		#print(self.norm_world_df)
		self.norm_world_df.Date = pd.to_datetime(self.norm_world_df.Date)
		self.norm_world_df = rename_columns(self.norm_world_df)
		#print(self.norm_world_df.datetime.min(), self.norm_world_df.datetime.max())
		#print(self.norm_world_df.region_id.isnull())

		for country, country_df in self.norm_world_df.groupby("country_id"):
			regions_df = country_df.copy()
			country_df = country_df.loc[country_df.region_id == "mainland"].fillna(0.0)
			country_df = add_missing_features_eng(country_df)
			self.countries_df_dict[country] = country_df
			self.countries_with_regions_df_dict[country] = {}
			for region, region_df in regions_df.groupby("region_id"):
				region_df = region_df.fillna(0.0)
				region_df = add_missing_features_eng(region_df)
				self.countries_with_regions_df_dict[country][region] = region_df.set_index("datetime")

	def plot_country_dashboard(self, country):
		country_path = os.path.join(
			world_figures_path,
			"countries",
			country
		)
		for region in self.countries_with_regions_df_dict[country]:
			df_region = self.countries_with_regions_df_dict[country][region]
			region_path = os.path.join(
				country_path,
				"regions",
				region
			)
			os.makedirs(region_path, exist_ok=True)
			plot_lines_dashboard(df_region, region_path, region, True)

	def save_norm(self):

		self.norm_world_df.to_csv(
			os.path.join(
				self.norm_data_path,
				"world_df.csv"
			)
		)

	def load_norm(self):

		data_path = os.path.join(
			self.norm_data_path,
			"world_df.csv"
		)
		self.norm_world_df = pd.read_csv(data_path, index_col=0)

