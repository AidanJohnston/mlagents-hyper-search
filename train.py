import argparse
from concurrent.futures import ProcessPoolExecutor
from logging import log
import multiprocessing
import os
import pickle
import time
from threading import Thread
from subprocess import Popen, CREATE_NEW_CONSOLE
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials, pyll

from scipy.stats import loguniform
from random import uniform
from MlagentsInstanceManager import MLManager

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('configFile', type=str,
                        help="The default config file each unity enviroment will build off of.")
    parser.add_argument("name", type=str,
                        help="Name of the trials run.")
    parser.add_argument('--configDir', required=False, default="./config/", type=str,
                        help="Folder for storing training config files.")
    parser.add_argument("--n-env", required=False, default=10, type=int,
                        help="Total number of environments to train.")
    parser.add_argument("--m-env", required=False, default=-1, type=int,
                        help="Maximum number of enivroments to launch at once. Set to -1 for n-menv == number of cpu cores.")
    parser.add_argument("--port", '-p', required=False, default=5005, type=int,
                        help="Initial port to use when launching environments.")
    parser.add_argument("--stopMinSteps", "--sms", required=False, default=500000, type=int,
                        help="Minimum number of steps to take before considering the early stopping condition.")
    parser.add_argument("--earlyStoppingSteps", "--ess", required=False, default=100000, type=int,
                        help="Amount of steps to take from the last recorded max before early stopping.")
    parser.add_argument("--earlyStoppingTag", '--est', required=False, default="Self-Play\\ELO", type=str,
                        help="Tensorboard tag to follow for early stopping")

    args = vars(parser.parse_args())


    mlagentsInstance = MLManager(args['configFile'],
                                   args['name'],
                                   configDir=args['configDir'],
                                   n_env=args['n_env'],
                                   m_env=args['m_env'],
                                   port=args['port'],
                                   stopMinSteps=args['stopMinSteps'],
                                   earlyStoppingSteps=args['earlyStoppingSteps'],
                                   earlyStoppingTag=args['earlyStoppingTag'])

    mlagentsInstance.run_trials()
if __name__ == "__main__":
    main()
