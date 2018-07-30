#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: autostart_vcenter
short_description: Configure autostart for vCenter VMs
options:
  name:
    description:
      - The name of the VM that needs to be configured
    required: true
    default: null
  hostname: 
    description
      - The target server that the VM and its host run on
      required: true
  username:
    description:
      - The vCenter username
    required: true
  password:
    description:
      - The vCenter password
    required: true
  esxi_host:
    description:
      - The ESXI host for the VM that is being configured
    required: true
  configuration
    description:
      - Whether or not to enable autostart for the VM
    required: false
    default: enable
    choices: ["enable", "disable"]
'''

EXAMPLES = '''
# Example for enabling autostart for vm_1
- autostart_vcenter:
    name: vm_1
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    esxi_host: esxi_ip
    configuration: enable

# Example for disabling or not enabling autostart for vm_1
- autostart_vcenter:
    name: vm_1
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    esxi_host: esxi_ip
    configuration: disable
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

def action_hosts(commaList, connection, startDelay, vmname, conf):
    print "Configuring provided hosts"
    acthosts = commaList.split(",")
    allhosts = get_hosts(connection)
    host_names = [h.name for h in allhosts]
    for a in acthosts:
        if a not in host_names:
            print "Host %s cannot be found" % a
    
    for h in allhosts:
        if h.name in acthosts:
            enable_autostart(h, startDelay, vmname, conf)

def enable_autostart(host, startDelay, vmname, conf):
    print "Enabling autostart for %s" % host.name
    hostDefSettings = vim.host.AutoStartManager.SystemDefaults()
    hostDefSettings.enabled = True 
    hostDefSettings.startDelay = int(startDelay)
    order = 1
    for vhost in host.vm:
        if vhost.name == vmname:
            spec = host.configManager.autoStartManager.config
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
                auto_power_info.startAction = 'powerOn' if  conf == 'enable' else 'None'
                auto_power_info.waitForHeartbeat = 'no'
                auto_power_info.startDelay = -1
                auto_power_info.startOrder = -1
                auto_power_info.stopAction = 'None'
                auto_power_info.stopDelay = -1
                spec.powerInfo = [auto_power_info]
                order = order + 1
                print "Applied settings to %s" % vhost
                host.configManager.autoStartManager.ReconfigureAutostart(spec)

def main():
    arg_spec = dict(
        name=dict(required=True, type='str'),
        hostname=dict(required=True, type='str'),
        username=dict(required=True, type='str'),
        password=dict(required=True, type='str'),
        esxi_host=dict(required=True, type='str'),
        configuration=dict(required=False, type='str')
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    
    start_delay = 10
    esxi_host = module.params['esxi_host']
    ip_addr = module.params['hostname']
    username = module.params['user']
    password = module.params['password']
    vm_name = module.params['name']
    conf = module.params['configuration']

    connection = get_connection(ip_addr, username, password)

    if esxi_host is not None:
        action_hosts(esxi_host, connection, start_delay, vm_name, conf)


main()
  
