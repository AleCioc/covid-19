import os
import json
import argparse

from bf_prelive_predictor.config.config import trainer_params_path
from bf_prelive_predictor.matches_descriptor.matches_descriptor import MatchesDescriptor
from bf_prelive_predictor.trainer.trainer import TimeSeriesTrainer

parser = argparse.ArgumentParser()

parser.add_argument (
	"-c", "--config_file_path",
	default="default_params.json",
	help="specify path of file containing training configuration"
)

parser.add_argument (
	"-s", "--save_model",
	default=True,
	action="store_true",
	help="save training model as a .pickle file on disk"
)

parser.add_argument(
	"-i", "--ids", nargs="+",
	help="specify the ids of matches to preprocess"
)

args = parser.parse_args()

descr = MatchesDescriptor()
descr.read()

if args.ids is None:
	train_matches_ids = [
		str(match_id) for match_id in descr.bf_matches_df.index[:10]
	]
else:
	train_matches_ids = args.ids

input_path = os.path.join(
	trainer_params_path,
	args.config_file_path
)
with open(input_path, 'r') as f:
	trainer_config = json.load(f)

trainer = TimeSeriesTrainer(
	trainer_config,
	train_matches_ids
)
trainer.train()

if args.save_model:
	trainer.save_final_estimator()
