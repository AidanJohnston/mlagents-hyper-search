import multiprocessing
import pickle
from subprocess import Popen, CREATE_NEW_CONSOLE

import yaml
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials, pyll
from jsonmerge import merge
import requests

from mlagentsInstance import mlagentsInstance


class MlagentsInstanceManager:

    def __init__(self,
                 defaultConfigFile,
                 trialsFile,
                 space,
                 configDir = "./config",
                 n_env = 10,
                 m_env = -1,
                 port = 5005,
                 stopMinSteps = 500000,
                 earlyStoppingSteps = 100000,
                 earlyStoppingTag = "Self-Play\\ELO"):
        '''
        :param defaultConfigFile:
        :param configDir:
        :param n_env:
        :param m_env:
        :param port:
        :param stopMinSteps:
        :param earlyStoppingSteps:
        :param earlyStoppingTag:
        '''
        self.defaultConfigFile = defaultConfigFile
        self.configDir = configDir
        self.n_env = n_env

        if m_env < 1:
            self.m_env = multiprocessing.cpu_count()
        else:
            self.m_env = m_env

        self.port = port
        self.stopMinSteps = stopMinSteps
        self.earlyStoppingSteps = earlyStoppingSteps
        self.earlyStoppingTag = earlyStoppingTag

        self.pTensorboard = self.__startTensorboardInstance__()

    def run_trials( reset=False):

        # attempt to load pickle file
        if not reset:
            try:
                # try to find file
                trials = pickle.load(open(filename, 'rb'))
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
        i = len(trials.trials)
        while i < max_evals:
            i = i + save_iter

            print(f"{i} of {max_evals}")
            best = fmin(fn=objective,
                        space=space,
                        algo=tpe.suggest,
                        max_evals=i,
                        trials=trials)

            with open(filename, 'wb') as f:
                pickle.dump(trials, f)
        return best


    def __startTensorboardInstance__(self):
        return Popen("tensorboard --logdir ./results")

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

    def __objective__(self, space):

        # Load YAML FILE
        with open(self.defaultConfigFile, 'r') as file:
            config = yaml.safe_load(file)


        _space = merge(config, space)

        filepath = ""
        name = ""
        port = 5005
        yaml.dump(_space, filepath)

        mlagentLearn = mlagentsInstance(filepath, name=name, port=port)

        while mlagentLearn.p.poll() is None:







