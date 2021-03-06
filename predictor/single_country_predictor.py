import pandas as pd

from predictor.errors import *
from utils.legend import *


class SingleCountryPredictor:

	def __init__(
			self,
			X_test,
			y_test,
			train_config,
			trainer,

	):

		self.config = train_config
		self.trainer = trainer
		self.X_test = X_test.astype(float).dropna()
		self.y_test = y_test.astype(float).dropna()
		self.y_hat_test = pd.Series()
		self.results_dict = {}

	def predict(self):
		self.y_hat_test = pd.Series(
			self.trainer.final_estimator.predict(self.X_test),
			index=self.X_test.index
		)

	def get_performance(self):
		summary_dict = {
			Errors.R_SQUARED: ErrorMetric(Errors.R_SQUARED, r2_score).compute(
				self.y_test, self.y_hat_test
			),
			Errors.ROOT_MEAN_SQUARED_ERROR: ErrorMetric(Errors.ROOT_MEAN_SQUARED_ERROR, rmse).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_ABSOLUTE_ERROR: ErrorMetric(Errors.MEAN_ABSOLUTE_ERROR, mean_absolute_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MAX_ABSOLUTE_ERROR: ErrorMetric(Errors.MAX_ABSOLUTE_ERROR, max_absolute_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_RELATIVE_ERROR: ErrorMetric(Errors.MEAN_RELATIVE_ERROR, mean_relative_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_ABSOLUTE_PERCENTAGE_ERROR: ErrorMetric(
				Errors.MEAN_ABSOLUTE_PERCENTAGE_ERROR, mean_absolute_percentage_error
			).compute(
				self.y_test, self.y_hat_test
			),
			Errors.SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR: ErrorMetric(
				SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR, sym_mape
			).compute(
				self.y_test, self.y_hat_test
			),
		}
		return pd.Series(summary_dict)
