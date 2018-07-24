#!/usr/bin/env python
'''
Script to configure autostart for vCenter VMs
'''

import argparse
import sys
import atexit
from pyVmomi import vim 
from pyVim.connect import Disconnect, SmartConnect
sys.dont_write_bytecode = True

def get_connection(ipAddr, user, password):
    try:
        connection = SmartConnect(
            host=ipAddr, port=443, user=user, pwd=password
        )
    except Exception as e:
        print e
        raise SystemExit
    return connection

def get_hosts(conn):
    print "Getting all host objects"
    content = conn.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    obj = [host for host in container.view]
    return obj

def action_hosts(commaList, connection, startDelay):
    print "Configuring provided hosts"
    acthosts = commaList.split(",")
    allhosts = get_hosts(connection)
    host_names = [h.name for h in allhosts]
    for a in acthosts:
        if a not in host_names:
            print "Host %s cannot be found" % a
    
    for h in allhosts:
        if h.name in acthosts:
            enable_autostart(host, startDelay)

def enable_autostart(host, startDelay):
    print "Enabling autostart for %s" % host.name
    hostDefSettings = vim.host.AutoStartManager.SystemDefaults()
    hostdefSettings.enabled = True 
    hostDefSettings.startDelay = int(startDelay)
    order = 1
    for vhost in host.vm:
        spec = host.configManager.AutoStartManager.config
        spec.defaults = hostDefSettings
        auto_power_info = vim.host.AutoStartManager.AutoPowerInfo()
        auto_power_info.key = vhost
        print "VM %s is updated if on" % vhost.name
        print "VM status is %s" % vhost.runtime.powerState
        if vhost.runtime.powerState == "poweredOff":
            auto_power_info.startAction = 'None'
            auto_power_info.waitForHeartbeat = 'no'
            auto_power_info.startDelay = -1
            auto_power_info.startOrder = -1
            auto_power_info.stopAction = 'None'
            auto_power_info.stopDelay = -1
        elif vhost.runtime.powerState == "poweredOn":
            auto_power_info.startAction = 'powerOn'
            auto_power_info.waitForHeartbeat = 'no'
            auto_power_info.startDelay = -1
            auto_power_info.startOrder = -1
            auto_power_info.stopAction = 'None'
            auto_power_info.stopDelay = -1
            spec.powerInfo = [auto_power_info]
            order = order + 1
            print "Applied settings to %s" % vhost
            host.configManager.AutoStartManager.ReconfigureAutostart(spec)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipAddr',
                        required=True,
                        action='store',
                        help='vCenter ESXI ip address')
    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='vCenter ESXI username')
    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='vCenter ESXI password')
    parser.add_argument('-t', '--actionhosts',
                        required=False,
                        action='store',
                        help='Comma delimited list of hosts whose VMs need to be configured')
    parser.add_argument('-d', '--startDelay',
                        required=False,
                        action='store',
                        default=10,
                        help='Default startup delay')
    args = parser.parse_args()
    print "Connecting to vCenter"
    connection = get_connection(args.ipAddr, args.user, args.password)

    if args.actionhosts is not None:
        action_hosts(args.actionhosts, connection, args.startDelay)

main()


