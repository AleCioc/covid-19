import git

from covid_19.data_manager.config.config import *


rawdatapath = os.path.join(os.getcwd(), "covid_19", "data_manager", "data", "raw", "cases", "italy", "COVID-19")

directory = os.listdir(rawdatapath)



# controllare se esiste la directory e clonare solo se non c'è
if not os.path.exists(rawdatapath) or len(directory) == 0:
    git.Repo.clone_from("https://github.com/pcm-dpc/COVID-19", rawdatapath)


g = git.cmd.Git(raw_cases_paths_dict["italy"])
g.pull()

#g = git.cmd.Git(raw_cases_paths_dict["world"])
#g.pull()
