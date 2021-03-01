import os
import json
import argparse
import multiprocessing as mp

import pandas as pd

from bf_prelive_predictor.config.config import *
from bf_prelive_predictor.matches_descriptor.matches_descriptor import MatchesDescriptor
from bf_prelive_predictor.model_validator.model_validator import run_model_validator
from bf_prelive_predictor.utils.datetime_utils import get_now_utc
from bf_prelive_predictor.utils.params_grid_utils import *
from bf_prelive_predictor.utils.path_utils import *


if __name__ == "__main__":

	mp.set_start_method('spawn')

	parser = argparse.ArgumentParser()

	parser.add_argument (
		"-m", "--run_mode",
		help="specify run mode"
	)

	parser.add_argument (
		"-c", "--config_file_path",
		help="specify path of file containing training configuration"
	)

	parser.add_argument(
		"-i", "--ids", nargs="+",
		help="specify the ids of matches for model validation"
	)

	parser.add_argument(
		"-n", "--n_matches",
		help="""
			specify the number of match markets to preprocess;
			matches are considered by sorted ids
		""",
		type=int
	)

	args = parser.parse_args()

	descr = MatchesDescriptor()
	descr.read()

	if args.ids is not None:
		validation_matches_ids = args.ids
	elif args.n_matches is not None:
		validation_matches_ids = [
			str(match_id) for match_id in descr.bf_matches_df.index[:args.n_matches]
		]
	else:
		validation_matches_ids = [
			str(match_id) for match_id in descr.bf_matches_df.index
		]

	if args.run_mode == "single_run":

		input_path = os.path.join(
			trainer_params_path,
			args.config_file_path
		)
		with open(input_path, 'r') as f:
			trainer_config = json.load(f)

		validators_input_dict = {
			"trainer_single_run_config": trainer_config,
			"match_ids": validation_matches_ids,
		}

		validator_summary = run_model_validator(validators_input_dict)

	elif args.run_mode == "multiple_runs":

		input_path = os.path.join(
			validator_params_grids_path,
			args.config_file_path
		)
		with open(input_path, 'r') as f:
			validators_params_grid_dict = json.load(f)
		validators_params_grid_list = config_grid_to_list_of_dict(validators_params_grid_dict)

		validators_input_dicts_list = []
		for i in range(len(validators_params_grid_list)):
			validators_input_dicts_list.append({
				"trainer_single_run_config": validators_params_grid_list[i],
				"match_ids": validation_matches_ids,
			})

		start_time = get_now_utc()

		with mp.Pool(n_cores) as pool:
			validators_output_list = pool.map(
				run_model_validator,
				validators_input_dicts_list
			)

		sim_stats_df = pd.concat([
			pd.DataFrame(sim_stats).T for sim_stats in validators_output_list
		], axis=0, ignore_index=True, sort=False)

		output_path = os.path.join(
			validation_results_path,
			"multiple_runs",
			get_string_from_conf_grid(validators_params_grid_dict),
		)
		check_create_path(output_path)

		sim_stats_df.to_csv(
			os.path.join(
				output_path,
				"sim_stats_df.csv"
			)
		)

		end_time = get_now_utc()

	print(end_time - start_time)
