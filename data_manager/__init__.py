import git

from data_manager.config.config import *


rawdatapath = os.path.join(os.getcwd(), "data_manager", "data", "raw", "cases", "italy")


directory = os.listdir(rawdatapath)

# controllare se esiste la directory e clonare solo se non c'è
if not os.path.exists(rawdatapath):
    git.Repo.clone_from("https://github.com/pcm-dpc/COVID-19", rawdatapath)


g = git.cmd.Git(raw_cases_paths_dict["italy"])
g.pull()

g = git.cmd.Git(raw_cases_paths_dict["world"])
g.pull()
