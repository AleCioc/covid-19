import os
import datetime

import pandas as pd

from bf_prelive_predictor.config.config import validation_results_path
from bf_prelive_predictor.preprocessor.multiple_matches_preprocessor import MultipleMatchesPreprocessor
from bf_prelive_predictor.matches_descriptor.matches_descriptor import MatchesDescriptor
from bf_prelive_predictor.trainer.trainer import TimeSeriesTrainer
from bf_prelive_predictor.predictor.single_match_predictor import SingleMatchPredictor
from bf_prelive_predictor.predictor.errors import *
from bf_prelive_predictor.plotter.regression_plotter import TimeSeriesRegressionPlotter
from bf_prelive_predictor.plotter.single_match_regression_plotter import SingleMatchRegressionPlotter
from bf_prelive_predictor.utils.path_utils import check_create_path
from bf_prelive_predictor.utils.data_prep_utils import create_df_features
from bf_prelive_predictor.utils.datetime_utils import get_now_utc
from bf_prelive_predictor.utils.legend import *
from bf_prelive_predictor.utils.params_grid_utils import *


def run_model_validator (validators_input_dict):

	match_ids = validators_input_dict["match_ids"]
	trainer_single_run_config = validators_input_dict["trainer_single_run_config"]

	validator = ModelValidator(
		trainer_single_run_config,
		match_ids,
	)

	validator.validate()

	return validator.summary


class ModelValidator:

	def __init__ (
			self,
			trainer_config,
			match_ids,
	):

		self.trainer_config = trainer_config
		self.match_ids = match_ids

		self.start = trainer_config["start"]
		self.depth = trainer_config["depth"]

		self.m_resampled_df = pd.DataFrame()
		self.X, self.y = self.create_regression_input()
		self.X_train = pd.DataFrame()
		self.X_test = pd.DataFrame()
		self.y_test = pd.Series()
		self.y_hat_test = pd.Series()

		self.dim_red_type = trainer_config["dim_red_type"]
		self.dim_red_param = trainer_config["dim_red_param"]
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

		self.descr = MatchesDescriptor()
		self.descr.read()

	def create_regression_input(self):

		prepro = MultipleMatchesPreprocessor(
			self.match_ids,
		)
		prepro.preprocess_matches(
			self.trainer_config["freq"],
			self.trainer_config["aggfunc_id"]
		)
		prepro.concat_resampled_markets(
			self.trainer_config["freq"],
			self.trainer_config["aggfunc_id"]
		)
		self.m_resampled_df = prepro.m_resampled_df

		cols = [
			col for col in self.m_resampled_df
			if col.endswith(traded_volume_suffix)
			or col.endswith(odd_suffix)
			or col.endswith(last_traded_price_suffix)
		]

		X = pd.DataFrame()
		for match_id, match_df in self.m_resampled_df.groupby(match_id_col_name):
			X_match = create_df_features(match_df, cols, self.trainer_config)
			X = pd.concat([X, X_match], sort=False)
		X[seconds_to_match_col_name] = self.m_resampled_df[seconds_to_match_col_name]
		for col in X:
			if col.endswith(traded_volume_suffix):
				X[col].fillna(0, inplace=True)
			if col.endswith(last_traded_price_suffix):
				X[col].fillna(1, inplace=True)
			if col.endswith(odd_suffix):
				X[col].fillna(1, inplace=True)
		y = self.m_resampled_df.loc[X.index, self.trainer_config["y_col"]]
		self.m_resampled_df = self.m_resampled_df.loc[X.index]

		return X, y

	def validate(self):

		start_time = get_now_utc()
		split_seq_n_index = []

		self.descr.bf_matches_df[match_id_col_name] = self.descr.bf_matches_df.index.astype(str).values
		self.descr.bf_matches_df.datetime = pd.to_datetime(self.descr.bf_matches_df.datetime)
		tested_matches_dict = {
			match_id: False for match_id in self.match_ids
		}

		for test_match in self.match_ids:

			train_matches = self.descr.bf_matches_df.loc[
				(self.descr.bf_matches_df.match_id != test_match) & (
					self.descr.bf_matches_df.datetime + datetime.timedelta(hours=2) < self.descr.bf_matches_df.loc[
						int(test_match), datetime_col_name
					]
				)
			].index.astype(str)

			train_index = self.m_resampled_df.loc[
				self.m_resampled_df.match_id.isin(train_matches)
			].index
			test_index = self.m_resampled_df.loc[
				self.m_resampled_df.match_id == test_match
			].index

			if len(train_index) and len(test_index):

				X_train = self.X.loc[train_index].copy()
				X_test = self.X.loc[test_index].copy()

				trainer = TimeSeriesTrainer(
					self.trainer_config,
					X_train,
					self.y.loc[train_index],

				)
				trainer.train()
				self.best_hyperparams += [trainer.best_hyperparams]

				test_index = self.m_resampled_df.loc[
					self.m_resampled_df.match_id == test_match
				].index
				predictor = SingleMatchPredictor(
					test_match,
					X_test.loc[:, trainer.chosen_features],
					self.y.loc[test_index],
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
				split_seq_n_index += [self.y.loc[test_index].index[0]]

				tested_matches_dict[test_match] = True

				match_regression_plotter = SingleMatchRegressionPlotter(
					test_match,
					predictor.y_test,
					predictor.y_hat_test,
					self.trainer_config,
				)
				match_regression_plotter.plot_charts()

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
