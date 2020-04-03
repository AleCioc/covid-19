from bf_prelive_predictor.plotter.regression_plotter import *
from bf_prelive_predictor.config.config import single_match_predictions_figures_path


class SingleMatchRegressionPlotter:

	def __init__(
			self,
			match_id,
			y_true,
			y_hat,
			trainer_config,
	):

		self.match_id = match_id
		self.y_true = y_true
		self.y_hat = y_hat
		self.trainer_config = trainer_config

		self.model_config_string = "_".join([str(v) for v in self.trainer_config.values()])
		for chart_id in ["y_pred_y_true", "residuals_hist"]:
			figures_path = os.path.join(
				root_figures_path,
				single_match_predictions_figures_path,
				self.model_config_string,
				chart_id
			)
			check_create_path(figures_path)
		self.figures_path = os.path.join(
			root_figures_path,
			single_match_predictions_figures_path,
			self.model_config_string,
		)

	def plot_charts(self):

		plot_result(self.y_true, self.y_hat, self.trainer_config["regr_type"])
		plt.tight_layout()
		plt.savefig(
			os.path.join(
				self.figures_path,
				"y_pred_y_true",
				self.match_id + ".png"
			)
		)
		plt.close()

		plot_residuals_hist(self.y_true, self.y_hat)
		plt.savefig(
			os.path.join(
				self.figures_path,
				"residuals_hist",
				self.match_id + ".png"
			)
		)
		plt.close()
