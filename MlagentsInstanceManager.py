import multiprocessing
import pickle
from subprocess import Popen, CREATE_NEW_CONSOLE

import yaml
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials, pyll
from jsonmerge import merge
import requests

from mlagentsInstance import mlagentsInstance


class MLManager:

    def __init__(self,
                 defaultConfigFile,
                 trialsFile,
                 configDir = "./config",
                 n_env = 10,
                 m_env = -1,
                 port = 5005,
                 stopMinSteps = 500000,
                 earlyStoppingSteps = 100000,
                 earlyStoppingTag = "Self-Play\\ELO",
                 reset=False):
        self.defaultConfigFile = defaultConfigFile
        self.trialsFile = trialsFile
        self.configDir = configDir
        self.n_env = n_env

        if m_env < 1:
            self.m_env = multiprocessing.cpu_count()
        else:
            self.m_env = m_env

        self.port = port
        self.reset = reset

        self.pTensorboard = self.__startTensorboardInstance__()

    def run_trials(self):

        # attempt to load pickle file
        if not self.reset:
            try:
                # try to find file
                trials = pickle.load(open(f"{self.trialsFile}.pickle", 'rb'))
                print(f"Trials file found.  Resuming from {len(trials.trials)} iterations.")
            except:
                # cant find
                trials = Trials()
                print("No Trials file found, will create new file.")

        # Dont attempt to load pickle file
        else:
            print("Reseting, will write over trials file.")
            trials = Trials()

        best = trials

        # iter untill max_evals is reached
        for i in range(len(trials.trials), self.n_env):

            augSpace = {"name": f"{self.trialsFile}_{i}",
                        "port": self.port + i,
                        "filepath": f"{self.trialsFile}_{i}.yaml",
                        "space": self.space}

            print(f"{i} of {self.n_env}")
            best = fmin(fn=__objective__,
                        space=augSpace,
                        algo=tpe.suggest,
                        max_evals=i,
                        trials=trials)

            with open(f"{self.trialsFile}.pickle", 'wb') as f:
                pickle.dump(trials, f)
        return best


    def __startTensorboardInstance__(self):
        return Popen("tensorboard --logdir ./results", creationflags=CREATE_NEW_CONSOLE)

    def tesnorboardHTTPCall(self, tag, name, behaviour):

        if self.pTensorboard is None:
            self.pTensorboard = self.__startTensorboardInstance__()

        apiURL = f"http://localhost:6006/data/plugin/scalars/scalars?tag={tag}&run={name}%5C{behaviour}"

        try:
            r = requests.get(apiURL)
            # Everything A OK
            if r.status_code == 200:
                return r.json()
        except:
            print("Could not connect to the tensorboard backend.")

def __objective__(space):

    # Load YAML FILE
    with open("./config/base.yaml", 'r') as file:
        config = yaml.safe_load(file)


    _space = merge(config, space["space"])
    yaml.dump(_space, space['filepath'])

    mlagentLearn = mlagentsInstance(space["filepath"], name=space["name"], port=space["port"])


    return {'loss': 0, 'status': STATUS_OK}