#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
#taken straight from centrify.dmc module
#https://github.com/centrify/dmc-python/blob/master/main.py
log.info("Going to test DMC config.")
log.info("Using endpoint /Security/Whoami/...")
check = other_requests(Call="/Security/Whoami").parsed_json
log.info("Tenant: {0}".format(check['Result']["TenantId"]))
log.info("User: {0}".format(check['Result']["User"]))
log.debug("UserUuid: {0}".format(check['Result']["UserUuid"]))