import os

import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams["axes.grid"] = True
plt.rcParams["figure.figsize"] = (15., 7)

from bf_prelive_predictor.utils.path_utils import check_create_path

from bf_prelive_predictor.extractor.bf_json_utils import get_market_outcomes


class SingleMatchPlotter:

	def __init__(self, prepro):

		self.prepro = prepro

		self.match_extracted_data_figures_path = os.path.join(
			self.prepro.match_extracted_data_path, "figures"
		)
		self.match_filtered_data_figures_path = os.path.join(
			self.prepro.match_filtered_data_path, "figures"
		)
		self.match_resampled_data_figures_path = os.path.join(
			self.prepro.match_resampled_data_path, "figures"
		)

		check_create_path(self.match_extracted_data_figures_path)
		check_create_path(self.match_filtered_data_figures_path)
		check_create_path(self.match_resampled_data_figures_path)

	def plot_column (self, df, col, title, figpath):
		plt.figure()
		plt.title(title)
		plt.xlabel("time")
		plt.ylabel(col)
		df[col].plot(marker="o")
		plt.savefig(os.path.join(figpath, col + ".png"))
		plt.close()

	def plot_events_tv(self):
		self.plot_column(
			self.prepro.events_df,
			"tv",
			"Cumulative traded volume by market events",
			self.match_extracted_data_figures_path
		)

	def plot_filtered_events_tv(self):
		self.plot_column(
			self.prepro.events_df_filtered,
			"tv",
			"Cumulative traded volume by market events filtered",
			self.match_filtered_data_figures_path
		)

	def plot_resampled_tv(self):
		self.plot_column(
			self.prepro.resampled_df,
			"tv",
			"Cumulative traded volume in time",
			self.match_resampled_data_figures_path

		)

	def plot_by_runner(self, market_df, col, title):
		outcomes = get_market_outcomes("MATCH_ODDS")
		fig, ax = plt.subplots()
		plt.title(title)
		plt.xlabel("time")
		plt.ylabel(col)
		for o in outcomes:
			market_df["_".join([o, col])].plot(ax=ax, marker="o")
		plt.legend()
		plt.show()
		plt.close()
