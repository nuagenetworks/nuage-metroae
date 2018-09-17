#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import sys
from pyVmomi import vim
from pyVim.connect import SmartConnect
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

# Example for disabling or not enabling autostart for vm_1
- vmware_autostart:
    name: vm_1
    uuid: vm_1_uuid
    hostname: target_server_ip
    username: vCenter_username
    password: vCenter_password
    state: disable
'''


def get_esxi_host(ipAddr, port, username, password, id):
    uuid = id
    try:
        si = get_connection(ipAddr, username, password, port)
        vm = si.content.searchIndex.FindByUuid(None,
                                               uuid,
                                               True,
                                               False)
    except Exception:
        return None

    if vm is not None:
        host = vm.runtime.host
        if host is not None:
            return host.name

    return None


def get_connection(ip_addr, user, password, port):
    try:
        connection = SmartConnect(
            host=ip_addr, port=port, user=user, pwd=password
        )
        return connection
    except Exception:
        return None


def get_hosts(conn):
    try:
        content = conn.RetrieveContent()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.HostSystem], True
        )
    except Exception:
        return None
    obj = [host for host in container.view]
    return obj


def configure_hosts(commaList, connection, startDelay, vmname, state):
    try:
        config_hosts = commaList.split(",")
        all_hosts = get_hosts(connection)
        host_names = [h.name for h in all_hosts]
        for a in config_hosts:
            if a not in host_names:
                return None
        for h in all_hosts:
            if h.name in config_hosts:
                return configure_autostart(h, startDelay, vmname, state)
    except Exception:
        return None


def configure_autostart(host, startDelay, vmname, state):
    hostDefSettings = vim.host.AutoStartManager.SystemDefaults()
    hostDefSettings.enabled = True
    hostDefSettings.startDelay = int(startDelay)
    order = 1
    if host is not None:
        try:
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
                        auto_power_info.startAction = 'powerOn' if state == 'enable' else 'None'
                        spec.powerInfo = [auto_power_info]
                        order = order + 1
                        host.configManager.autoStartManager.ReconfigureAutostart(spec)
                    return True
        except Exception:
            return False


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
            delay=dict(required=False, type=int, default=10)
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

    connection = get_connection(ip_addr, username, password, port)

    if connection is None:
        module.fail_json(changed=False, msg="Could not connect to %s" % ip_addr)

    esxi_host = get_esxi_host(ip_addr, port, username, password, uuid)

    if esxi_host is not None:
        configured = configure_hosts(esxi_host, connection, start_delay, vm_name, state)
    else:
        module.fail_json(changed=False, msg="Could not get ESXi host for %s" % vm_name)

    if configured:
        module.exit_json(changed=True, msg="VM %s has been configured" % vm_name)
    else:
        module.fail_json(changed=False, msg="VM %s could not be configured" % vm_name)

if __name__ == "__main__":
    main()
