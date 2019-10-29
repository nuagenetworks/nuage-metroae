#!/usr/bin/env python
import os
from pathlib2 import Path
import tarfile
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--tarFileName', default='files_test')
parser.add_argument('--deploymentName', default='/deployments')
args = parser.parse_args()
tarFileName=args.tarFileName
deploymentName=args.deploymentName
cwdir=os.getcwd()
ansibleLogPath=Path(cwdir+'/ansible.log')
with tarfile.open( tarFileName + '.tar.gz', mode='w:gz') as archive:
    # archive.add( cwdir + '/deployments/' + deploymentName, arcname='/unzipped/deployments/'+deploymentName,recursive=True)
    try:
        archive.add( cwdir + '/deployments/' + deploymentName, arcname='/unzipped/deployments/'+deploymentName,recursive=True)
        
    except:
        print("deployment directory doenst exits")
    try:
        archive.add(cwdir+'/src/inventory', arcname='/unzipped/src/inventory',recursive=True)
    except:
        print("Inventory doesn't exist")
    if ansibleLogPath.exists():
        archive.add(cwdir+'/ansible.log',arcname='/unzipped/ansible.log')
    else:
        print("ansible.log file doesn't exist")
    



