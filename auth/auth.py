#!/usr/bin/env python3
import json
import os
import argparse
from paspymod.logger import logging as log
from paspymod.utility import getConfigPath
import getpass

def cl():
    parser = argparse.ArgumentParser(description="API Auth config maker. Makes JSON file in current workers dir")
    parser.add_argument('-a','--auth', type=str, required=True, help= 'dmc OR oauth')
    parser.add_argument('-s','--scope', type=str, required=True, help= 'scope of token')
    parser.add_argument('-t','--tenant', type=str, required=True, help= 'abc0123.my.centrify.net') 
    parser.add_argument('-aid','--appid', type=str, required=False, help= 'app id of the oauth token')
    parser.add_argument('-sa','--service_account', type=str, required=False, help= 'service account of the token')
    parser.add_argument('-p','--password', type=str, required=False, default=None, help= 'pw of service account')
    parser.add_argument('-wp','--write_pw_to_file', type=bool, required=False, default=False, help= 'will save pw to file')
    parser.add_argument('-d','--debug', type=str, required=False, default='DEBUG', help= 'set debug level. Options: DEBUG, INFO, WARNING, ERROR. Default is DEBUG.')
    return parser.parse_args()
if __name__ == "__main__":
    args = vars(cl())

def saveConfig(path = getConfigPath().real_path):
    if args['auth'].upper() == 'OAUTH':
        dictionary =  {'auth' : 'OAUTH','urls' : {'tenant': args['tenant'],'app_url': '{tenant}/Oauth2/Token/{appid}'.format(**args)},'body': {'scope': args['scope'],\
            'client_id': args['service_account'], 'grant_type': 'client_credentials'}, 'debug_level': args['debug']}
        if args['write_pw_to_file'] == True:
            try:
                dictionary['body']['client_secret'] = args['password']
            except KeyError:
                log.error("Need to input PW value")
                raise Exception
            pass
        try:
            with open(path, "w", encoding='utf-8') as conf:
                conf.write(json.dumps(dictionary, sort_keys=True, indent = 4))
                #maybe permissions
                pass
            pass
        except:
            log.error("Error making oauth JSON config File")
            raise Exception
    if args['auth'].upper() == 'DMC':
        with open(path, "w+") as conf:
            try:
                conf.write(json.dumps({'auth':'DMC', 'scope':args['scope'], 'urls' : {'tenant': args['tenant']}, 'debug_level': args['debug']}, sort_keys=True, indent=4))
                log.info('Made the DMC config file.')
                #maybe permissions
            except:
                log.error("Cannot Make file for DMC auth.")
                raise Exception
            pass
        pass
    else:
        log.warning('Not a valid auth type. Please use DMC or OAUTH')
        return {}
saveConfig()

