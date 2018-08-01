#!/usr/bin/python

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
  uuid:
    description:
      - The UUID of the VM to configure
    required: true
    default: null
  hostname: 
    description
      - The target server that the VM and its host run on
      required: true
  port:
    description:
      - The port on which to connect
    required: false
    default: 443
  username:
    description:
      - The vCenter username
    required: true
  password:
    description:
      - The vCenter password
    required: true
  state
    description:
      - Whether or not to enable autostart for the VM
    required: false
    default: "None"
    choices: ["enable", "disable"]
  delay:
    description:
      - Time, in seconds, for delayed start of the VM
    required: false
    default: 10

'''

EXAMPLES = '''
# Example for enabling autostart for vm_1
- autostart_vcenter:
    name: vm_1
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    state: enable

# Example for disabling or not enabling autostart for vm_1
- autostart_vcenter:
    name: vm_1
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    state: disable
'''

import subprocess
import argparse
import sys
import atexit
from pyVmomi import vim
from pyVim.connect import Disconnect, SmartConnect
sys.dont_write_bytecode = True

def get_esxi_host(ipAddr, port, username, password, id):
    uuid = id
    si = None
    si = get_connection(ipAddr, username, password, port)
    if si == -1:
        desired_state = -1
        return desired_state
    vm = si.content.searchIndex.FindByUuid(None,
                                           uuid,
                                           True,
                                           False)
    if vm is not None:
        host = vm.runtime.host
    else:
        host = None
    host_ip = host.name
    return host_ip

def get_connection(ip_addr, user, password, port):
    try:
        connection = SmartConnect(
            host=ip_addr, port=port, user=user, pwd=password
        )
    except Exception:
        desired_state = -1
        return desired_state

    return connection

def get_hosts(conn):
    content = conn.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    obj = [host for host in container.view]
    return obj

def configure_hosts(commaList, connection, startDelay, vmname, state):
    config_hosts = commaList.split(",")
    all_hosts = get_hosts(connection)
    host_names = [h.name for h in all_hosts]
    for a in config_hosts:
        if a not in host_names:
            desired_state = -1
    
    for h in all_hosts:
        if h.name in config_hosts:
            desired_state = configure_autostart(h, startDelay, vmname, state)

    return desired_state

def configure_autostart(host, startDelay, vmname, state):
    desired_state = -1
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
            auto_power_info.waitForHeartbeat = 'no'
            auto_power_info.startDelay = -1
            auto_power_info.startOrder = -1
            auto_power_info.stopAction = 'None'
            auto_power_info.stopDelay = -1
            if vhost.runtime.powerState == "poweredOff":
                auto_power_info.startAction = 'None'
            elif vhost.runtime.powerState == "poweredOn":
                auto_power_info.startAction = 'powerOn' if  state == 'enable' else 'None'
                spec.powerInfo = [auto_power_info]
                order = order + 1
                host.configManager.autoStartManager.ReconfigureAutostart(spec)
                desired_state = 0
    return desired_state

def main():
    arg_spec = dict(
        name=dict(required=True, type='str'),
        uuid=dict(required=True, type='str'),
        hostname=dict(required=True, type='str'),
        port=dict(required=False, type=int, default=443),
        username=dict(required=True, type='str', no_log=True),
        password=dict(required=True, type='str', no_log=True),
        state=dict(required=False, type='str', default='None'),
        delay=dict(required=False, type=int, default=10)
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    
    ip_addr = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    vm_name = module.params['name']
    state = module.params['state']
    uuid = module.params['uuid']
    port = module.params['port']
    start_delay = module.params['delay']
    desired_state = -1

    connection = get_connection(ip_addr, username, password, port)

    if connection == -1:
        module.fail_json(changed=False, msg="Could not connect to %s" % ip_addr)

    esxi_host = get_esxi_host(ip_addr, port, username, password, uuid)

    if esxi_host != -1:
        desired_state = configure_hosts(esxi_host, connection, start_delay, vm_name, state)
    elif esxi_host == -1:
        module.fail_json(changed=False, msg="Could not get ESXi host for %s" % vm_name)

    if desired_state == 0:
        module.exit_json(changed=True, msg="VM %s has been configured" % vm_name)
    else:
        module.fail_json(changed=False, msg="VM %s could not be configured" % vm_name)

if __name__ == "__main__":        
    main()
  
