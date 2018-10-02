#!/usr/bin/python

import os
from ansible.module_utils.basic import AnsibleModule
import sys
from pyVmomi import vim
from pyVim.connect import SmartConnect
from pyVim.connect import SmartConnectNoSSL
sys.dont_write_bytecode = True


DOCUMENTATION = '''
---
module: vmware_autostart
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
    required: true
    choices: ["enable", "disable"]
  delay:
    description:
      - Delay in seconds before continuing with the next
        virtual machine in the order to be started
    required: false
    default: 10
  validate_certs:
    description:
      - Whether Ansible should validate ssh certificates
    required: False
    default: True

'''

EXAMPLES = '''
# Example for enabling autostart for vm_1
- vmware_autostart:
    name: vm_1
    uuid: vm_1_uuid
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    state: enable
    validate_certs: False

# Example for disabling or not enabling autostart for vm_1
- vmware_autostart:
    name: vm_1
    uuid: vm_1_uuid
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    state: disable
'''


def get_esxi_host(ip_addr, port, username, password, id, validate_certs):
    uuid = id
    si = get_connection(ip_addr, username, password, port, validate_certs)
    vm = si.content.searchIndex.FindByUuid(None,
                                           uuid,
                                           True,
                                           False)
    if vm is not None:
        host = vm.runtime.host
        if host is not None:
            return host.name

    return None


def get_connection(ip_addr, user, password, port, validate_certs):
    if validate_certs:
        connection = SmartConnect(
            host=ip_addr, port=port, user=user, pwd=password)
    else:
        connection = SmartConnectNoSSL(
            host=ip_addr, port=port, user=user, pwd=password)
    return connection


def get_host_obj(host_name, conn):
    obj = None
    content = conn.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    for c in container.view:
        if c.name == host_name:
            obj = c
            break
    return obj


def configure_autostart(host_name, connection, start_delay, vmname, state):
    host_obj = get_host_obj(host_name, connection)
    if host_obj is None:
        return {'failed': True, 'msg': 'Could not find {0} in list of hosts'.format(host_name)}
    vm_names = [vm.name for vm in host_obj.vm]
    if vmname not in vm_names:
        return {'failed': True, 'msg': 'Could not find {0} in list of VMs'.format(vmname)}
    host_def_settings = vim.host.AutoStartManager.SystemDefaults()
    host_def_settings.enabled = True
    host_def_settings.startDelay = int(start_delay)
    for vm in host_obj.vm:
        if vm.name == vmname:
            spec = host_obj.configManager.autoStartManager.config
            spec.defaults = host_def_settings
            auto_power_info = vim.host.AutoStartManager.AutoPowerInfo()
            auto_power_info.key = vm
            auto_power_info.waitForHeartbeat = 'no'
            auto_power_info.startDelay = -1
            auto_power_info.startOrder = -1
            auto_power_info.stopAction = 'None'
            auto_power_info.stopDelay = -1
            if vm.runtime.powerState == "poweredOff":
                auto_power_info.startAction = 'None'
            elif vm.runtime.powerState == "poweredOn":
                auto_power_info.startAction = 'powerOn' if state == 'enable' else 'None'
                spec.powerInfo = [auto_power_info]
                host_obj.configManager.autoStartManager.ReconfigureAutostart(spec)
    return {'failed': False, 'msg': 'Autostart change initiated for {0}'.format(vmname)}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(
                type='str',
                default=os.environ.get('VMWARE_HOST')
            ),
            username=dict(
                type='str',
                default=os.environ.get('VMWARE_USER')
            ),
            password=dict(
                type='str', no_log=True,
                default=os.environ.get('VMWARE_PASSWORD')
            ),
            validate_certs=dict(required=False, type='bool', default=True),
            name=dict(required=True, type='str'),
            uuid=dict(required=False, type='str'),
            port=dict(required=False, type=int, default=443),
            delay=dict(required=False, type=int, default=10),
            state=dict(required=True, type='str', choices=['enable', 'disable'])
        ),
    )

    ip_addr = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    vm_name = module.params['name']
    state = module.params['state']
    uuid = module.params['uuid']
    port = module.params['port']
    start_delay = module.params['delay']
    validate_certs = module.params['validate_certs']

    try:
        connection = get_connection(ip_addr, username, password, port, validate_certs)

        if connection is None:
            module.fail_json(msg="Establishing connection to %s failed" % ip_addr)

        esxi_host = get_esxi_host(ip_addr, port, username, password, uuid, validate_certs)

        if esxi_host is None:
            module.fail_json(msg="Could not find ESXi host using uuid %s" % uuid)

        result = configure_autostart(esxi_host, connection, start_delay, vm_name, state)
    except:
        e = sys.exec_info()[0]
        module.fail_json(msg="Attempt to configure autostart failed with exception: %s" % e)

    if result['failed']:
        module.fail_json(**result)
    else:
        module.exit_json(**result)

if __name__ == "__main__":
    main()
