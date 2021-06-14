from paspymod.funct_tools import query_request, other_requests, sanitizedict, rem_null
from paspymod.logger import logging as log
import argparse
import ast
import os 
import csv

# https://developer.centrify.com/reference#post_servermanage-updateresource
# Workaround to bug:
# CPSSUP-1047
# BE SURE TO USE A FILE AS THAT IS COMMA SEPARATED VALUE FILE AND NOT UTF ENCODED. WILL THROW OFF THE CSV HEADER READ. 

def cl():
    parser = argparse.ArgumentParser(description="Update a resource.")
    parser.add_argument('-p','--Path', type=str, required=False, help= 'Path to a CSV file of the systems to update. Please follow the same structure as in example files.')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())

path = os.path.abspath(args['Path'])
log.info("Path to the csv file to add resources is: {0}".format(path))
with open(path, 'r') as f:
    d_reader = csv.DictReader(f)
    for line in d_reader:
        log.info("Querying for ID to use on system whose name is: {0}".format(line['Name']))
        id_q = query_request(sql = "Select Server.ID From Server Where Server.Name = '{0}'".format(line['Name'])).parsed_json
        if id_q["Result"]["Count"] == 0:
            log.error("System not found")
        else:
            log.info("Found ID for system for: {0}".format(line['Name']))
            id = id_q["Result"]["Results"][0]["Row"]['ID']
        query = query_request(sql = "Select * From Server Where Server.ID = '{0}'".format(id)).parsed_json
        for x in query["Result"]["Results"]:
            if x["Row"] != None:
                wanted = x["Row"]
        new_args = rem_null(wanted)
        new_args['ProxyUserIsManaged'] = False
        new_args['ProxyUser'] = ""
        print(new_args['ProxyUserIsManaged'])
        other_requests(Call='/ServerManage/UpdateResource', **new_args, Debug=True)