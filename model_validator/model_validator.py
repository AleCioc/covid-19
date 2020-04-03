import os
import datetime

import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

from config.config import validation_results_path
from trainer.trainer import TimeSeriesTrainer
from predictor.single_country_predictor import SingleCountryPredictor
from predictor.errors import *
from utils.data_prep_utils import *
from utils.path_utils import *
from utils.datetime_utils import *
from utils.legend import *
from utils.params_grid_utils import *


def run_model_validator (validators_input_dict):

	country_df = validators_input_dict["country_df"]
	validator_params_dict = validators_input_dict["validator_params_dict"]

	validator = ModelValidator(
		country_df,
		validator_params_dict,
	)

	validator.validate()

	return validator.summary


class ModelValidator:

	def __init__ (
		self,
		world_df,
		validator_params,
	):

		self.X = pd.DataFrame()
		self.y = pd.Series()
		country_count = 0
		for country, country_df in world_df.groupby("country_id"):

			day_threshold_cases = country_df[
				country_df.total_cases > 100
			].datetime.min()

			country_df["day_threshold_cases"] = (
					country_df.datetime - day_threshold_cases
			).apply(lambda td: td.days)

			country_df = country_df[country_df.day_threshold_cases > 0]

			if len(country_df) > 0:
				country_count += 1

			X_country = create_df_features(
				country_df,
				[
					"day_threshold_cases",
					"total_deaths",
					"total_recovered",
					"total_cases",
				],
				validator_params
			)
			X_country["datetime"] = country_df["datetime"]
			#X_country["health_exp_public_pct_2016"] = country_df["health_exp_public_pct_2016"]
			#X_country["per_capita_exp_ppp_2016"] = country_df["per_capita_exp_ppp_2016"]
			#X_country["densita_pop"] = country_df["densita_pop"]

			y_country = country_df[validator_params["y_col"]].loc[X_country.index]
			self.X = pd.concat([
				self.X, X_country
			], ignore_index=True)
			self.y = pd.concat([
				self.y, y_country
			], ignore_index=True)

		self.X = self.X.sort_values("datetime")
		self.X = self.X.drop("datetime", axis=1).dropna()
		self.y = self.y.loc[self.X.index]
		print(country_count)
		print(self.X.shape, self.y.shape)

		self.X_train = pd.DataFrame()
		self.y_train = pd.Series()

		self.X_test = pd.DataFrame()
		self.y_test = pd.Series()
		self.y_hat_test = pd.Series()

		self.trainer_config = validator_params

		self.training_policy = validator_params["training_policy"]
		self.training_size = validator_params["training_size"]
		self.training_update_t = validator_params["training_update_t"]

		self.dim_red_type = validator_params["dim_red_type"]
		self.dim_red_param = validator_params["dim_red_param"]
		self.dim_red_scores = pd.DataFrame()
		self.feature_coefs_model = pd.DataFrame(columns=self.X.columns)
		self.chosen_features = []
		self.dim_red_scores = pd.DataFrame()

		self.cv_results = pd.DataFrame()
		self.best_hyperparams = []

		self.summary = pd.Series()

		self.output_path = os.path.join(
			validation_results_path,
			"single_run",
			get_string_from_conf(self.trainer_config)
		)
		check_create_path(self.output_path)

		self.validation_time = datetime.timedelta()

	def validate(self):
		
		if self.training_policy == "sliding":
			tscv = TimeSeriesSplit(
				n_splits = (len(self.X)-1)//self.training_update_t,
				max_train_size = self.training_size
			)
		elif self.training_policy == "expanding":
			tscv = TimeSeriesSplit(
				n_splits = (len(self.X)-1)//self.training_update_t
			)

		split_seq_n_index = []

		start_time = get_now_utc()

		for train_index, test_index in tscv.split(self.X):

			if len(train_index) < self.training_size:
				continue

			X_train = self.X.iloc[train_index].copy()
			X_test = self.X.iloc[test_index].copy()

			trainer = TimeSeriesTrainer(
				self.trainer_config,
				X_train,
				self.y.iloc[train_index],
			)
			trainer.train()
			self.best_hyperparams += [trainer.best_hyperparams]

			predictor = SingleCountryPredictor(
				X_test.loc[:, trainer.chosen_features],
				self.y.iloc[test_index],
				self.trainer_config,
				trainer
			)
			predictor.predict()

			self.X_test = pd.concat([self.X_test, predictor.X_test], sort=False)
			self.y_test = pd.concat([self.y_test, predictor.y_test], sort=False)
			self.y_hat_test = pd.concat([self.y_hat_test, predictor.y_hat_test])
			self.y_hat_test.loc[self.y_hat_test < 0] = 0
			self.cv_results = pd.concat(
				[self.cv_results, pd.DataFrame(trainer.cv_results)],
				ignore_index=True, sort=False
			)
			self.dim_red_scores = pd.concat(
				[self.dim_red_scores, pd.DataFrame(trainer.dim_red_scores).T],
				sort=False
			)
			self.feature_coefs_model = pd.concat(
				[self.feature_coefs_model, pd.DataFrame(trainer.regression_coefs).T],
				ignore_index=True, sort=False
			)
			split_seq_n_index += [self.y.iloc[test_index].index[0]]

		self.validation_time = (get_now_utc() - start_time).total_seconds()
		self.summary = self.get_performance()
		self.best_hyperparams = pd.DataFrame(self.best_hyperparams)
		self.save_output()

	def get_performance(self):

		self.y_test = self.y_test.loc[self.y_hat_test.index]

		summary_dict = self.trainer_config

		summary_dict.update({
			Errors.R_SQUARED.value: ErrorMetric(Errors.R_SQUARED, r2_score).compute(
				self.y_test, self.y_hat_test
			),
			Errors.ROOT_MEAN_SQUARED_ERROR.value: ErrorMetric(Errors.ROOT_MEAN_SQUARED_ERROR.value, rmse).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_ABSOLUTE_ERROR.value: ErrorMetric(Errors.MEAN_ABSOLUTE_ERROR.value, mean_absolute_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MAX_ABSOLUTE_ERROR.value: ErrorMetric(Errors.MAX_ABSOLUTE_ERROR.value, max_absolute_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_RELATIVE_ERROR.value: ErrorMetric(Errors.MEAN_RELATIVE_ERROR.value, mean_relative_error).compute(
				self.y_test, self.y_hat_test
			),
			Errors.MEAN_ABSOLUTE_PERCENTAGE_ERROR.value: ErrorMetric(
				Errors.MEAN_ABSOLUTE_PERCENTAGE_ERROR.value, mean_absolute_percentage_error
			).compute(
				self.y_test, self.y_hat_test
			),
			Errors.SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR.value: ErrorMetric(
				Errors.SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR.value, sym_mape
			).compute(
				self.y_test, self.y_hat_test
			),
		})

		if self.trainer_config["hyperparams_tuning"] == 1:
			summary_dict["mean_fit_time"] = self.cv_results.mean_fit_time.mean()
		summary_dict["validation_time"] = self.validation_time

		return pd.Series(summary_dict)

	def save_output(self):

		def _to_csv(pd_obj, csv_name):
			pd_obj.to_csv(
				os.path.join(
					self.output_path,
					csv_name
				), header=True
			)

		_to_csv(self.y_test, "y_test.csv")
		_to_csv(self.y_hat_test, "y_hat_test.csv")
		_to_csv(self.summary, "summary.csv")
		_to_csv(self.cv_results, "cv_results.csv")
		_to_csv(self.best_hyperparams, "best_hyperparams.csv")
		_to_csv(self.best_hyperparams.mode(), "best_hyperparams_mode.csv")
		_to_csv(self.dim_red_scores, "dim_red_scores.csv")
		_to_csv(self.dim_red_scores.mean(), "dim_red_scores_mean.csv")
		_to_csv(self.feature_coefs_model, "feature_coefs.csv")
		_to_csv(self.feature_coefs_model.mean(), "feature_coefs_mean.csv")
