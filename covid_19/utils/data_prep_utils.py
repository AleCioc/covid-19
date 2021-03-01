import pandas as pd


def get_past_lags(series, start, depth):
	return pd.concat([
		pd.Series(series.shift(i), name=series.name + "_-" + str(i))
		for i in range(start, start + depth)
	], axis=1)


def create_df_features(X, cols, trainer_config):

	start = trainer_config['start']
	depth = trainer_config['depth']
	df_features = pd.DataFrame(index=X.index)

	for col in cols:
		lagged_df = get_past_lags(X[col], start, depth)
		df_features = pd.concat([
			df_features, lagged_df],
			axis=1, sort=False
		)

	return df_features.dropna()
