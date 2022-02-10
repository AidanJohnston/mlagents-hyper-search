import argparse
from concurrent.futures import ProcessPoolExecutor
from logging import log
import multiprocessing
import os
import pickle
import time
from threading import Thread
from subprocess import Popen, CREATE_NEW_CONSOLE



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configFile', '--cf', required=True, type=str,
                        help="The configFile with search parameters defined.  If no configDir is being the folder of "
                             "this file be used as output for test config files.")
    parser.add_argument('--nenv', '--ne', required=False, default=10)
    parser.add_argument('--port', '--p', required=False, default=5005)
    parser.add_argument('--stopMinSteps', '--sms', type=int, required=False, default=100000, metavar="N",
                        help="Minimum steps to take before considering the early stopping condition.")
    parser.add_argument("--earlyStoppingSteps", '--ess', default=50000, required=False, type=int, metavar='N',
                        help="The amount of steps after the max before early stopping the enviroment.")
    parser.add_argument('--earlyStoppingTag' '--est', required=False, default="Self-Play\\ELO")

    args = vars(parser.parse_args())

    # Check if file exits
    if not os.path.isfile(args['configFile']):
        raise FileNotFoundError("Could not find " + args['configFile'])

    

if __name__ == "__main__":
    main()
