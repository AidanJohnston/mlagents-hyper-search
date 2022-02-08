import os
import string
from subprocess import Popen, CREATE_NEW_CONSOLE
import argparse
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configDir', '--cd', required=False, type=str,
                        help="The folder where test config files will be stored.")
    parser.add_argument('--configFile', '--cf', required=True, type=str,
                        help="The configFile with search parameters defined.  If no configDir is being the folder of "
                             "this file be used as output for test config files.")

    args = vars(parser.parse_args())

    # Check if file exits
    if not os.path.isfile(args['configFile']):
        raise FileNotFoundError("Could not find " + args['configFile'])

    # If Config folder not set use cf folder
    if args['configDir'] is None:
        args['configDir'] = os.path.dirname(args['configFile'])

    # Check if folder exits
    elif not os.path.isdir(args['configDir']):
        raise NotADirectoryError("Could not find " + args['configDir'])

    # Loading yaml file
    with open(args['configFile'], 'r') as file:
        configFile = yaml.safe_load(file)


    print(args)
if __name__ == "__main__":
    main()
