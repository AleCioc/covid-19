import git

from data_manager.config.config import *

g = git.cmd.Git(raw_cases_paths_dict["italy"])
g.pull()
