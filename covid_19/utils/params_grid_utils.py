import itertools


def config_grid_to_list_of_dict(json_conf_grid):

	conf_list = []
	for el in itertools.product(*json_conf_grid.values()):
		conf = {k: None for k in json_conf_grid}
		i = 0
		for k in conf.keys():
			conf[k] = el[i]
			i += 1
		conf_list += [conf]
	return conf_list


def get_string_from_conf(trainer_params):
	model_conf_string = "_".join([
		str(v) for v in trainer_params.values()]
	).replace("'", "").replace(".", "d")
	return model_conf_string


def get_string_from_conf_grid(validator_params_grid):
	model_conf_string = "_".join([
		str(v) for v in validator_params_grid.values()
	]).replace(" ", "-").replace("'", "").replace(".", "d").replace(",", "-").replace("[", "-").replace("]", "-")
	return model_conf_string
