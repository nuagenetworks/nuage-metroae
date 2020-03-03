#!/usr/bin/env python
import os
import tarfile
import argparse
from time import gmtime, strftime

cwdir = os.getcwd()
run_mode = "container"
if(os.path.isfile(os.path.join(cwdir,'ansible.cfg'))):
    run_mode = "repo"

now = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
parser = argparse.ArgumentParser(description='This script collects the debug collateral in a tarball')
parser.add_argument('--tarFileName', default='debug-' + now)
parser.add_argument('--deploymentName')
args = parser.parse_args()
tarFileName = args.tarFileName
if args.deploymentName:
    deploymentName = os.path.join("deployments", args.deploymentName)
else:
    deploymentName = "deployments"

if run_mode == "repo":
    ansibleLogPath = os.path.join(cwdir, 'ansible.log')
    deploymentPath = os.path.join(cwdir, deploymentName)
    inventoryPath = os.path.join(cwdir, 'src/inventory')
else:
    ansibleLogPath = os.path.join(cwdir, 'nuage-metro', 'ansible.log')
    deploymentPath = os.path.join(cwdir, 'nuage-metro', deploymentName)
    inventoryPath = os.path.join(cwdir, 'nuage-metro', 'src/inventory')
    tarFileName = os.path.join('/metroae_data', tarFileName)

with tarfile.open(tarFileName + '.tar.gz', mode='w:gz') as archive:
    try:
        archive.add(deploymentPath, arcname=os.path.join('/unzipped/', deploymentName), recursive=True)
    except:
        print("Deployment not found")
    try:
        archive.add(inventoryPath, arcname='/unzipped/src/inventory', recursive=True)
    except:
        print("Inventory not found")
    if os.path.exists(ansibleLogPath) and os.path.isfile(ansibleLogPath):
        archive.add(ansibleLogPath, arcname='/unzipped/ansible.log')
    else:
        print("ansible.log not found")
