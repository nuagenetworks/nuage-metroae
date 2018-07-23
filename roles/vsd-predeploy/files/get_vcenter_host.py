#!/usr/bin/env python
import subprocess
import argparse
from pyVmomi import vim
from pyVim import connect
from pyVim.connect import SmartConnect

def main():
    parser = argparse.ArgumentParser(description='Process args to retrieve VMs')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use to connect to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use to connect to host')
    
    args = parser.parse_args()
    proc = subprocess.Popen(["sudo dmidecode|grep UUID|awk '{print $2}'"], 
                            stdout=subprocess.PIPE,
                            shell=True)
    out, err = proc.communicate()
    uuid = out[:-1]

    si = None
    si = connect.SmartConnect(host=args.host,
                              user=args.user,
                              pwd=args.password,
                              port=args.port)

    vm = si.content.searchIndex.FindbyUuid(None,
                                           uuid,
                                           True,
                                           False)
    host = vm.runtime.host 

    return host

main()