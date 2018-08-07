#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware import connect_to_api, gather_vm_facts, wait_for_task

HAS_PYVMOMI = False
try:
    from pyVmomi import vim

    HAS_PYVMOMI = True
except ImportError:
    pass

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: vmware_nic_connection
short_description: Connect or disconnect a nic of a VM
description:
    - Connect or disconnect a nic of a VM
version_added: 2.4
author:
    - Philippe Dellaert <philippe@dellaert.org>
notes:
    - Tested on vSphere 6.5
requirements:
    - "python >= 2.6"
    - PyVmomi
options:
   name:
        description:
            - Name of the VM to work with
        required: True
   name_match:
        description:
            - If multiple VMs matching the name, use the first or last found
        default: 'first'
        choices: ['first', 'last']
   uuid:
        description:
            - UUID of the instance to manage if known, this is VMware's unique identifier.
            - This is required if name is not supplied.
   folder:
        description:
            - Destination folder, absolute path to find an existing guest.
            - This is required if name is supplied.
   datacenter:
        description:
            - Destination datacenter for the deploy operation
        required: True
   nic_mac:
        description:
            - The MAC address of the nic to connect/disconnect
   all_nics:
        description:
            - If this is set to true, all nics states will be changed
        default: false
        choices: [true, false]
   state:
        description:
            - State of the nic, can be connected or disconnected
        choices: ['connected', 'disconnected']
        required: True
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = '''
- name: Connect a nic
  vmware_nic_connection:
    hostname: 192.168.1.209
    username: administrator@vsphere.local
    password: vmware
    validate_certs: no
    uuid: 421e4592-c069-924d-ce20-7e7533fab926
    nic_mac: 00:50:56:a4:94:f1
    state: connected
  delegate_to: localhost
  register: facts

- name: Disconnect all nics
  vmware_nic_connection:
    hostname: 192.168.1.209
    username: administrator@vsphere.local
    password: vmware
    validate_certs: no
    uuid: 421e4592-c069-924d-ce20-7e7533fab926
    all_nics: yes
    state: disconnected
  delegate_to: localhost
  register: facts
'''

RETURN = """
instance:
    description: metadata about the virtual machine
    returned: always
    type: dict
    sample: None
"""


class VmwareNicManager(object):
    def __init__(self, module):
        if not HAS_PYVMOMI:
            module.fail_json(msg='pyvmomi module required')

        self.module = module
        self.content = connect_to_api(self.module)

    def getvm(self):
        si = self.content.searchIndex
        vm = None

        if self.module.params.get('uuid'):
            vm = si.FindByUuid(instanceUuid=False, uuid=self.module.params.get('uuid'), vmSearch=True)
        elif self.module.params.get('folder'):
            # Build the absolute folder path to pass into the search method
            if not self.module.params.get('folder').startswith('/'):
                self.module.fail_json(msg="Folder %(folder)s needs to be an absolute path, starting with '/'." % self.module.params)
            searchpath = '%(datacenter)s%(folder)s' % self.module.params

            # get all objects for this path ...
            f_obj = self.content.searchIndex.FindByInventoryPath(searchpath)
            if f_obj:
                if isinstance(f_obj, vim.Datacenter):
                    f_obj = f_obj.vmFolder
                for c_obj in f_obj.childEntity:
                    if not isinstance(c_obj, vim.VirtualMachine):
                        continue
                    if c_obj.name == self.module.params.get('name'):
                        vm = c_obj
                        if self.module.params.get('name_match') == 'first':
                            break
        return vm

    def find_nics(self, vm):
        nics = list()
        for dev in vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                if self.module.params.get('all_nics'):
                    nics.append(dev)
                elif dev.macAddress.lower() == self.module.params.get('nic_mac').lower():
                    nics.append(dev)
                    break
        return nics

    def ensure(self):
        results = dict(changed=False, instance=None)
        changes = []
        state = self.module.params.get('state')
        vm = self.getvm()
        nics = self.find_nics(vm=vm)
        for nic in nics:
            if (state == 'connected' and not nic.connectable.connected) or (state == 'disconnected' and nic.connectable.connected):
                nic_spec = vim.vm.device.VirtualDeviceSpec()
                nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                nic_spec.device = nic
                nic_spec.device.key = nic.key
                nic_spec.device.macAddress = nic.macAddress
                nic_spec.device.backing = nic.backing
                nic_spec.device.wakeOnLanEnabled = nic.wakeOnLanEnabled
                connectable = vim.vm.device.VirtualDevice.ConnectInfo()
                if state == 'connected':
                    connectable.connected = True
                    connectable.startConnected = True
                elif state == 'disconnected':
                    connectable.connected = False
                    connectable.startConnected = False
                nic_spec.device.connectable = connectable
                changes.append(nic_spec)
        if len(changes) > 0:
            spec = vim.vm.ConfigSpec()
            spec.deviceChange = changes
            task = vm.ReconfigVM_Task(spec=spec)

            wait_for_task(task)
            results['changed'] = True
        results['instance'] = gather_vm_facts(self.content, vm)
        self.module.exit_json(**results)


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
            name_match=dict(required=False, type='str', default='first'),
            uuid=dict(required=False, type='str'),
            folder=dict(required=False, type='str', default='/vm'),
            datacenter=dict(required=True, type='str'),
            nic_mac=dict(required=False, type=str),
            all_nics=dict(required=False, type='bool', default=False),
            state=dict(required=True, type='str', choices=['connected', 'disconnected'])
        ),
    )

    # Prepend /vm if it was missing from the folder path, also strip trailing slashes
    if not module.params['folder'].startswith('/vm') and module.params['folder'].startswith('/'):
        module.params['folder'] = '/vm%(folder)s' % module.params
    module.params['folder'] = module.params['folder'].rstrip('/')

    vmware_nic_manager = VmwareNicManager(module)
    vmware_nic_manager.ensure()

if __name__ == '__main__':
    main()
