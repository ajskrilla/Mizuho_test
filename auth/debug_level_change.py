#!/usr/bin/env python3
from paspymod.logger import logging as log
from paspymod.utility import getConfigPath
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change log level.")
    parser.add_argument('-l','--Level', type=str, required=True, help= 'Log Level. DEBUG, INFO, WARNING, ERROR')
    args = parser.parse_args()

def update_log_level(path = getConfigPath().real_path):
    with open(path, 'r') as json_file:
        config = json.load(json_file)
        config['debug_level'] = args.Level
    with open(path, "w") as json_file:
        json_file.write(json.dumps(config, sort_keys=True, indent = 4))

update_log_level()