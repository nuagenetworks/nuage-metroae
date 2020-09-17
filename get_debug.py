#!/usr/bin/env python
import os
import tarfile
import argparse
import re
from time import gmtime, strftime
cwdir = os.getcwd()
run_mode = "container"
if(os.path.isfile(os.path.join(cwdir, 'ansible.cfg'))):
    run_mode = "repo"
now = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
parser = argparse.ArgumentParser(description='This script collects the debug collateral in a tarball')
parser.add_argument('--tarFileName', default='debug-' + now)
parser.add_argument('--deploymentName')
args = parser.parse_args()
tarFileName = args.tarFileName
print("The name of the tar file created:" + tarFileName + ".tar.gz")
if args.deploymentName:
    deploymentName = os.path.join("deployments", args.deploymentName)
else:
    deploymentName = "deployments"
if run_mode == "repo":
    ansibleLogPath = os.path.join(cwdir, 'ansible.log')
    deploymentPath = os.path.join(cwdir, deploymentName)
    inventoryPath = os.path.join(cwdir, 'src/inventory')
    print('The log path is:' + cwdir + '/metroae_data/' + tarFileName + ".tar.gz")
else:
    ansibleLogPath = os.path.join(cwdir, 'nuage-metroae', 'ansible.log')
    deploymentPath = os.path.join(cwdir, 'nuage-metroae', deploymentName)
    inventoryPath = os.path.join(cwdir, 'nuage-metroae', 'src/inventory')
    tarFileName = os.path.join(cwdir, '/metroae_data', tarFileName)
    print('The log path is:' + cwdir + '/metroae_data/' + tarFileName + ".tar.gz")
with tarfile.open(tarFileName + '.tar.gz', mode='w:gz') as archive:
    try:
        archive.add(deploymentPath, arcname=os.path.join('/unzipped/', deploymentName), recursive=True)
    except:
        print("Can't find" + deploymentName + "Skipping.")
    try:
        archive.add(inventoryPath, arcname='/unzipped/src/inventory', recursive=True)
    except:
        print("Inventory not found")
    if os.path.exists(ansibleLogPath) and os.path.isfile(ansibleLogPath):
        archive.add(ansibleLogPath, arcname='/unzipped/ansible.log')
    else:
        print("Can't find ansible.log, Skipping.")
command = "tar -tvf " + tarFileName + ".tar.gz >files.txt"
os.system(command)
f=open("files.txt" , "r" )
fread = f.read()
outlist=re.findall("unzipped/.*/.*/(.*)" , fread)
for i in outlist:
    if( i == '' ):
        outlist.remove(i)
print("The files included in the " + tarFileName + ".tar.gz are:")
for i in outlist:
    if( i == '' ):
        continue
    else:
        print(i)
