hyperparams_grids = {
	"lr": {
		"normalize": [True, False],
		"fit_intercept": [True, False]
	},
	"ridge": {
		"normalize": [True, False],
		"fit_intercept": [True, False],
		"alpha": [0.01, 0.1, 1]
	},
	"lsvr": {
		"C": [1, 10, 100, 1000],
		"max_iter": [1500]
	},
	"svr": {
		"kernel": ["rbf"],
		"gamma": ["scale"],
		"C": [1, 10, 100, 1000],
		"max_iter": [1500]
	},
	"rf": {
		"random_state": [1],
		"n_estimators": [75, 80, 85, 90],
	}
}
