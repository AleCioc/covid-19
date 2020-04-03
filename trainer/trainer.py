import os
import joblib

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import mutual_info_regression

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import make_scorer

from bf_prelive_predictor.config.config import trainer_pickles_path
from bf_prelive_predictor.trainer.hyperparams_grids import hyperparams_grids
from bf_prelive_predictor.trainer.best_hyperparams import best_hyperparams

from bf_prelive_predictor.utils.legend import *


def crosscorr (X, y):
	return pd.DataFrame(X).apply(lambda x: x.corr(pd.Series(y))).values


class TimeSeriesTrainer:

	def __init__(
			self,
			trainer_config,
			X_train,
			y_train,
	):

		self.config = trainer_config

		self.m_resampled_df = pd.DataFrame()
		self.X = X_train
		self.y = y_train

		self.regr = None
		self.scorers = None
		self.scaler = None
		self.hyperparams_grid = None
		self.search = None
		self.dim_reduction = None
		self.chosen_features = self.X.columns
		self.dim_red_scores = pd.DataFrame(index=self.X.columns)

		self.steps = []
		self.pipeline = None
		self.best_pipeline = None
		self.best_regressor = None
		self.best_hyperparams = {}
		self.final_estimator = None

		self.regression_coefs = pd.Series()
		self.cv_results = pd.DataFrame()

	def get_scaler(self):
		if self.config["scaler_type"] == Scalers.STANDARD.value:
			return StandardScaler()
		if self.config["scaler_type"] == Scalers.MINMAX.value:
			return MinMaxScaler()
		raise Exception("{} Invalid scaler type!".format(self.config["scaler_type"]))

	def get_regressor(self):
		if self.config["regr_type"] == Regressors.LINEAR.value:
			return LinearRegression()
		if self.config["regr_type"] == Regressors.RIDGE.value:
			return Ridge()
		if self.config["regr_type"] == Regressors.LINEAR_SVR.value:
			return LinearSVR()
		if self.config["regr_type"] == Regressors.GAUSSIAN_SVR.value:
			return SVR()
		if self.config["regr_type"] == Regressors.RANDOM_FOREST.value:
			return RandomForestRegressor()
		raise Exception("{} Invalid regression type!".format(self.config["regr_type"]))

	def get_dim_reduction(self):

		if self.config["dim_red_type"] == FeatureSelectors.CROSS_CORRELATION.value:
			return SelectKBest(
				crosscorr,
				self.config["dim_red_param"]
			)
		if self.config["dim_red_type"] == FeatureSelectors.MUTUAL_INFORMATION.value:
			return SelectKBest(
				mutual_info_regression,
				self.config["dim_red_param"]
			)
		if self.config["dim_red_type"] == FeatureSelectors.MODEL_COEFFICIENTS.value:
			return SelectFromModel(
				self.regr,
				threshold=-np.inf,
				max_features=self.config["dim_red_param"]
			)
		#raise Exception("{} Invalid dimensionality reduction type!".format(self.config["dim_red_type"]))

	def get_scorers(self):
		
		return [
			ErrorMetric("mean_absolute_error", make_scorer(mean_absolute_error)).to_dict(),
		]

	def get_hyperparams_grid(self):

		self.hyperparams_grid = hyperparams_grids[
			self.config["regr_type"]
		]

		new_grid = {}
		for k in self.hyperparams_grid.keys():
			new_grid[PipelineSteps.REGRESSION.value + "__" + str(k)] = self.hyperparams_grid[k]
		self.hyperparams_grid = new_grid

	def get_hyperparams_grid_search(self):
		self.search = GridSearchCV(
			self.pipeline,
			self.hyperparams_grid,
			cv=3,
			return_train_score=False,
		)

	def get_dim_red_results(self):

		if self.config["dim_red_type"] in [
			FeatureSelectors.CROSS_CORRELATION.value,
			FeatureSelectors.MUTUAL_INFORMATION.value,
			FeatureSelectors.MODEL_COEFFICIENTS.value
		]:
			self.chosen_features = self.X.loc[
				:, self.final_estimator.named_steps[PipelineSteps.DIMENSIONALITY_REDUCTION.value].get_support()
			].columns

		if self.config["dim_red_type"] in [
			FeatureSelectors.CROSS_CORRELATION.value,
			FeatureSelectors.MUTUAL_INFORMATION.value
		]:
			self.dim_red_scores = pd.Series(
				self.final_estimator.named_steps[PipelineSteps.DIMENSIONALITY_REDUCTION.value].scores_,
				index=self.X.columns
			)
			self.dim_red_scores = self.dim_red_scores.loc[self.chosen_features]

	def get_regression_coefs(self):

		if self.config["regr_type"] in [
			Regressors.LINEAR.value,
			Regressors.LINEAR_SVR.value
		]:
			self.regression_coefs = pd.Series(
				self.best_regressor.coef_,
				index=self.chosen_features
			)
		elif self.config["regr_type"] in [
			Regressors.RANDOM_FOREST.value
		]:
			self.regression_coefs = pd.Series(
				self.best_regressor.feature_importances_.tolist(),
				index=self.chosen_features
			)

	def get_best_params_regressor(self):

		if self.config["hyperparams_tuning"] != "best":
			best_hyperparams = {}
			for k in self.best_hyperparams.keys():
				best_hyperparams[k.split("__")[1]] = self.best_hyperparams[k]
		else:
			best_hyperparams = self.best_hyperparams

		if self.config["regr_type"] == Regressors.LINEAR.value:
			return LinearRegression(**best_hyperparams)
		elif self.config["regr_type"] == Regressors.LINEAR_SVR.value:
			return LinearSVR(**best_hyperparams)
		elif self.config["regr_type"] == Regressors.RANDOM_FOREST.value:
			return RandomForestRegressor(**best_hyperparams)

	def train(self):

		self.regr = self.get_regressor()
		self.scorers = self.get_scorers()
		self.scaler = self.get_scaler()
		self.dim_reduction = self.get_dim_reduction()

		if self.config["hyperparams_tuning"] == HyperparamsTuningOptions.ACTIVE.value:
			if self.config["scaler_type"] != "":
				self.steps.append((PipelineSteps.SCALER.value, self.scaler))
			self.steps.append((PipelineSteps.DIMENSIONALITY_REDUCTION.value, self.dim_reduction))
			self.steps.append((PipelineSteps.REGRESSION.value, self.regr))
			self.pipeline = Pipeline(self.steps)
			self.get_hyperparams_grid()
			self.get_hyperparams_grid_search()
			self.search.fit(self.X, self.y)
			self.cv_results = self.search.cv_results_
			self.best_hyperparams = self.search.best_params_
			self.best_pipeline = self.search.best_estimator_
			self.best_regressor = self.best_pipeline.named_steps[PipelineSteps.REGRESSION.value]
			self.search.fit(self.X.loc[:, self.chosen_features], self.y)
			self.final_estimator = self.best_pipeline
		else:
			if self.config["hyperparams_tuning"] == HyperparamsTuningOptions.BEST_FOUND_PARAMS.value and self.config[
				"regr_type"
			] in best_hyperparams:
				self.best_hyperparams = best_hyperparams[self.config["regr_type"]]
				self.best_regressor = self.get_best_params_regressor()
				self.steps = []
				if self.config["scaler_type"] != "":
					self.steps.append((PipelineSteps.SCALER.value, self.scaler))
				self.steps.append((PipelineSteps.DIMENSIONALITY_REDUCTION.value, self.dim_reduction))
				self.steps.append((PipelineSteps.REGRESSION.value, self.best_regressor))
				self.pipeline = Pipeline(self.steps)
				self.pipeline.fit(self.X, self.y)
			else:
				if self.config["scaler_type"] != "":
					self.steps.append((PipelineSteps.SCALER.value, self.scaler))
				self.steps.append((PipelineSteps.DIMENSIONALITY_REDUCTION.value, self.dim_reduction))
				self.steps.append((PipelineSteps.REGRESSION.value, self.regr))
				self.pipeline = Pipeline(self.steps)
				self.best_regressor = self.regr
				self.best_hyperparams = self.regr.get_params()
				self.pipeline.fit(self.X, self.y)
			self.final_estimator = self.pipeline
		self.get_dim_red_results()
		self.final_model = self.final_estimator.fit(self.X.loc[:, self.chosen_features], self.y)
		self.get_regression_coefs()

	def save_final_estimator (self):
		model_conf_string = "_".join([str(v) for v in self.config.values()])
		out_pickle_filename = os.path.join(
			trainer_pickles_path,
			model_conf_string
		)
		joblib.dump(
			self.final_model,
			filename=out_pickle_filename
		)
