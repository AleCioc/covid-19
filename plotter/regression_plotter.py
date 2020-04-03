import os

import pandas as pd
import matplotlib.pyplot as plt

from bf_prelive_predictor.utils.path_utils import check_create_path
from bf_prelive_predictor.config.config import root_figures_path


def plot_residuals(y_true, y_pred):

	residuals = y_true - y_pred
	residuals = pd.DataFrame(residuals)

	fig1, ax1 = plt.subplots(figsize=(13,8))
	plt.title('Residual errors in time', fontsize = 18, y=1.03)
	plt.plot(residuals)
	plt.grid()
	ax1.tick_params(axis='y', labelsize=14)
	ax1.tick_params(axis='x', labelsize=14)
	plt.xlabel('Model no.', fontsize=16, labelpad=15)
	plt.ylabel('Residual error', fontsize=16, labelpad=15)
	plt.tight_layout()
	plt.grid()


def plot_residuals_hist(y_true, y_pred):

	fig2, ax2 = plt.subplots(figsize=(9,6))
	residuals = y_true - y_pred
	plt.hist(residuals, bins=50)
	plt.grid(axis='both')
	ax2.tick_params(axis='y', labelsize=14)
	ax2.tick_params(axis='x', labelsize=14)
	plt.xlabel('Residual error', fontsize=16, labelpad=15)
	plt.ylabel('Frequency', fontsize=16, labelpad=15)
	plt.title('Residual errors histogram', fontsize = 18, y=1.03)
	plt.tight_layout()


def plot_result(y_data, y_pred_series, alg):

	fig, ax = plt.subplots(figsize=(15,7))
	plt.title('Real values v.s predicted values', fontsize = 18, y=1.03)
	plt.ylabel('ODD', fontsize=16, labelpad=15)

	plt.xlabel('t', fontsize=16, labelpad=15)

	if alg == 'lr': label_alg = 'Linear Regression'
	elif alg == 'ridge': label_alg = 'Ridge Regression'
	elif alg == 'omp': label_alg = 'Orthogonal Matching Pursuit'
	elif alg == 'brr': label_alg = 'Bayesian Ridge Regression'
	elif alg == 'lsvr': label_alg = 'Linear Support Vector Regression'
	elif alg == 'svr': label_alg = 'Support Vector Regression'
	elif alg == 'rf': label_alg = 'Random Forest Regression'

	ax.plot(y_data, color='g', marker="o", label='True Values')
	ax.plot(y_pred_series, color='coral', marker="o", label=label_alg)

	ax.tick_params(axis='y', labelsize=14)
	ax.tick_params(axis='x', labelsize=14)
	plt.legend(loc=1, fontsize=14)
	plt.tight_layout()
	plt.grid()


class TimeSeriesRegressionPlotter:

	def __init__(
			self,
			y_true,
			y_hat,
			trainer_config,
	):

		self.y_true = y_true
		self.y_hat = y_hat
		self.trainer_config = trainer_config

		self.model_config_string = "_".join([str(v) for v in self.trainer_config.values()])
		self.figures_path = os.path.join(
			root_figures_path,
			self.model_config_string
		)
		check_create_path(self.figures_path)

	def plot_charts(self):

		plot_result(self.y_true, self.y_hat, self.trainer_config["regr_type"])
		plt.tight_layout()
		plt.savefig(
			os.path.join(
				self.figures_path,
				"y_pred_y_true.png"
			)
		)
		plt.close()

		plot_residuals_hist(self.y_true, self.y_hat)
		plt.savefig(
			os.path.join(
				self.figures_path,
				"residuals_hist.png"
			)
		)
		plt.close()
