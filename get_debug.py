#!/usr/bin/env python
import os
import tarfile
import argparse
from time import gmtime, strftime
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

cwdir = os.getcwd()
ansibleLogPath = os.path.join(cwdir, 'ansible.log')
with tarfile.open(tarFileName + '.tar.gz', mode='w:gz') as archive:
    try:
        archive.add(os.path.join(cwdir, deploymentName), arcname=os.path.join('/unzipped/', deploymentName), recursive=True)
    except:
        print("Deployment not found")
    try:
        archive.add(os.path.join(cwdir, 'src/inventory'), arcname='/unzipped/src/inventory', recursive=True)
    except:
        print("Inventory not found")
    if os.path.exists(ansibleLogPath) and os.path.isfile(ansibleLogPath):
        archive.add(os.path.join(cwdir, 'ansible.log'), arcname='/unzipped/ansible.log')
    else:
        print("ansible.log not found")
