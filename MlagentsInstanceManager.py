import multiprocessing
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from subprocess import Popen, CREATE_NEW_CONSOLE

import yaml
from jsonmerge import merge
from scipy.stats import loguniform
from random import uniform


class MLManager:

    def __init__(self,
                 defaultConfigFile,
                 configDir="./config/",
                 n_env=10,
                 m_env=-1,
                 port=5005,
                 reset=False):
        self.defaultConfigFile = defaultConfigFile
        self.configDir = configDir
        self.n_env = n_env

        if m_env < 1:
            self.m_env = multiprocessing.cpu_count()
        else:
            self.m_env = m_env

        self.port = port
        self.reset = reset

    def run_trials(self):

        spaces = []
        # generate info for all trials
        for i in range(self.n_env):
            space = {}
            space['space'] = {
                "behaviors": {
                    "Player": {
                        "hyperparameters": {
                            "learning_rate": float(loguniform(0.00001, 0.1).rvs()),
                            "beta": float(loguniform(0.0001, 0.1).rvs()),
                            "epsilon": uniform(0.1, 0.3),
                            "lambd": uniform(0.9, 0.95)
                        },
                        "reward_signals": {
                            "extrinsic": {
                                "gamma": uniform(0.9, 0.995)
                            },
                            "curiosity": {
                                "strength": uniform(0.1, 0.3),
                                "gamma": uniform(0.9, 0.995),
                                "learning_rate": float(loguniform(0.00001, 0.1).rvs())
                            }
                        }
                    }
                }
            }

            space['name'] = str(uuid.uuid4())
            space['filepath'] = f"{self.configDir}{space['name']}.yaml"
            space['port'] = self.port + i
            space['defaultConfigFile'] = self.defaultConfigFile
            spaces.append(space)

        with ProcessPoolExecutor(max_workers=self.m_env) as executor:
            results = executor.map(trial, spaces)

def trial(space):

    print(f"Starting Unity Environment {space['name']} on localhost:{space['port']}")

    with open(space['defaultConfigFile'], "r") as file:
        config = yaml.safe_load(file)

    _space = merge(config, space['space'])

    with open(space['filepath'], "w") as file:
        yaml.dump(_space, file)

    print(f"mlagents-learn {space['filepath']} --run-id={space['name']} --base-port={space['port']}")
    p = Popen(f"mlagents-learn {space['filepath']} --run-id={space['name']} --base-port={space['port']}",
              creationflags=CREATE_NEW_CONSOLE)

    while p.poll() is None:
        time.sleep(15)

    return