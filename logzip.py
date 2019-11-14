#!/usr/bin/env python
import os
from pathlib2 import Path
import tarfile
import argparse
from time import gmtime, strftime
now = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
parser = argparse.ArgumentParser()
parser.add_argument('--tarFileName', default='debug-' + now)
parser.add_argument('--deploymentName')
args = parser.parse_args()
tarFileName = args.tarFileName
if args.deploymentName:
    deploymentName = "/deployments/" + args.deploymentName
else:
    deploymentName = "/deployments/"

cwdir = os.getcwd()
ansibleLogPath = Path(cwdir + '/ansible.log')
with tarfile.open( tarFileName + '.tar.gz', mode = 'w:gz') as archive:
    try:
        archive.add( cwdir + deploymentName, arcname = '/unzipped/'+deploymentName,recursive=True)
    except:
        print("deployment directory doenst exits")
    try:
        archive.add(cwdir + '/src/inventory', arcname = '/unzipped/src/inventory',recursive=True)
    except:
        print("Inventory doesn't exist")
    if ansibleLogPath.exists():
        archive.add(cwdir + '/ansible.log',arcname = '/unzipped/ansible.log')
    else:
        print("ansible.log file doesn't exist")
    



