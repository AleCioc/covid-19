import git

from covid_19.data_manager.config.config import *

def pull():
    g = git.cmd.Git(raw_cases_paths_dict["italy"])
    g.pull()
    #pulizia di cose inutili
    directory = os.listdir(rawdatapath)
    for subdirectory in directory:
        if subdirectory in ["aree", "dati-json", "dati-province", "note", "dati-contratti-dpc-forniture", "schede-iss"]:
            import shutil
            shutil.rmtree(os.path.join(raw_cases_paths_dict["italy"], subdirectory))
            print("\tRimossa "+str(subdirectory))



rawdatapath = os.path.join(os.getcwd(), "covid_19", "data_manager", "data", "raw", "cases", "italy", "COVID-19")

directory = os.listdir(rawdatapath)

# controllare se esiste la directory e clonare solo se non c'è
if not os.path.exists(rawdatapath) or len(directory) == 0:
    #git.Repo.clone_from("https://github.com/pcm-dpc/COVID-19", rawdatapath)

    repo = " https://github.com/pcm-dpc/COVID-19"
    folder = "./data"
    print(rawdatapath)
    print(os.curdir)
    projectname = "COVID-19"
    branch = "master"
    directories = "dati-regioni/* dati-andamento-nazionale/* "
    cmd = "bash clone.sh git_sparse_checkout "+ repo+" "+ folder+" "+projectname+" "+branch+" "+directories
    os.system(cmd)
    import shutil
    from_p = os.path.join(os.curdir, "data", "COVID-19")
    to_p = os.path.join(os.curdir, "covid_19", "data_manager", "data", "raw", "cases", "italy")
    shutil.rmtree(os.path.join(to_p, "COVID-19"))
    shutil.move(from_p, to_p)
    shutil.rmtree(os.path.join(os.curdir, "data"))

pull()


#g = git.cmd.Git(raw_cases_paths_dict["world"])
#g.pull()


