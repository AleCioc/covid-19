from enum import Enum


class PipelineSteps(Enum):
    REGRESSION = "regressor"
    SCALER = "scaler"
    DIMENSIONALITY_REDUCTION = "dim_reduction"


class Scalers(Enum):
    STANDARD = "std"
    MINMAX = "minmax"


class Regressors(Enum):
    LINEAR = "lr"
    RIDGE = "ridge"
    LINEAR_SVR = "lsvr"
    GAUSSIAN_SVR = "svr"
    RANDOM_FOREST = "rf"


class FeatureSelectors(Enum):
    CROSS_CORRELATION = "crosscorr"
    MUTUAL_INFORMATION = "mutinf"
    MODEL_COEFFICIENTS = "model"


class HyperparamsTuningOptions(Enum):
    NOT_ACTIVE = 0
    ACTIVE = 1
    BEST_FOUND_PARAMS = "best"


class Errors(Enum):
    R_SQUARED = "r2"
    ROOT_MEAN_SQUARED_ERROR = "rmse"
    MEAN_ABSOLUTE_ERROR = "mae"
    MAX_ABSOLUTE_ERROR = "mxae"
    MEAN_RELATIVE_ERROR = "mre"
    MEAN_ABSOLUTE_PERCENTAGE_ERROR = "mape"
    SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR = "smape"


class ErrorMetric:

    def __init__(self, name, scorer_func):

        self.name = name
        self.scorer_func = scorer_func

    def compute(self, y_true, y_hat):
        return self.scorer_func(y_true, y_hat)

    def to_dict(self):
        return {self.name: self.scorer_func}


traded_volume_suffix = "tv"
last_traded_price_suffix = "ltp"
odd_suffix = "odd"

match_id_col_name = "match_id"
seconds_to_match_col_name = "seconds_to_match"
datetime_col_name = "datetime"

betfair_1x2_market_id = "MATCH_ODDS"