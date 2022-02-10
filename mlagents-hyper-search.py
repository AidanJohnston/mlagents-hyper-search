import argparse
from concurrent.futures import ProcessPoolExecutor
from logging import log
import multiprocessing
import os
import pickle
import time
from threading import Thread
from subprocess import Popen, CREATE_NEW_CONSOLE

class MlagentsHyperSearch():

    def __init__(self, config, name, nenv, configDir = "./config/", basePort = 5005):
        self.config = config
        self.name = name
        self.nenv = nenv
        self.configDir = configDir
        self.basePort = basePort

        for i in list(range(1, nenv + 1)):

            p = Popen(f"mlagents-learn {self.config} --run-id={self.name}_{i} --base-port={self.basePort + i}",
                      creationflags=CREATE_NEW_CONSOLE)
            while p.poll() is None:
                time.sleep(10)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configFile', '--cf', required=True, type=str,
                        help="The configFile with search parameters defined.  If no configDir is being the folder of "
                             "this file be used as output for test config files.")
    parser.add_argument('--nenv', '--ne', required=False, default=10)
    parser.add_argument('--port', '--p', required=False, default=5005)
    args = vars(parser.parse_args())

    # Check if file exits
    if not os.path.isfile(args['configFile']):
        raise FileNotFoundError("Could not find " + args['configFile'])

    mlagentsHyperSearch = MlagentsHyperSearch(args['configFile'], "testRun", 10, basePort=5005)

if __name__ == "__main__":
    main()
