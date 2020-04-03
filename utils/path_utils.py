import os


def check_create_path (path):
	os.makedirs(path, exist_ok=True)


def check_create_match_path (base_path, match_id):
	check_create_path(
		os.path.join(base_path, match_id)
	)


def check_create_match_paths (base_path, match_ids):
	check_create_path(base_path)
	for match_id in match_ids:
		check_create_match_path(base_path, match_id)


def delete_data_path(data_path):
	if os.path.exists(data_path):
		os.system("rm -r " + data_path)
