#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This module is also sponsored by E.T.A.I. (www.etai.fr)
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
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils.vmware import connect_to_api, gather_vm_facts

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
module: vmware_guest_tools_wait
short_description: Wait for VMware tools to become available and return facts
description:
    - Wait for VMware tools to become available on the VM and return facts
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
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = '''
- name: Wait for VMware tools to become available
  vmware_guest_tools_wait:
    hostname: 192.168.1.209
    username: administrator@vsphere.local
    password: vmware
    validate_certs: no
    uuid: 421e4592-c069-924d-ce20-7e7533fab926
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


class PyVmomiHelper(object):
    def __init__(self, module):
        if not HAS_PYVMOMI:
            module.fail_json(msg='pyvmomi module required')

        self.module = module
        self.params = module.params
        self.content = connect_to_api(self.module)

    def getvm(self, name=None, uuid=None, folder=None):
        si = self.content.searchIndex
        vm = None

        if uuid:
            vm = si.FindByUuid(instanceUuid=False, uuid=uuid, vmSearch=True)
        elif folder:
            # Build the absolute folder path to pass into the search method
            if not self.params['folder'].startswith('/'):
                self.module.fail_json(msg="Folder %(folder)s needs to be an absolute path, starting with '/'." % self.params)
            searchpath = '%(datacenter)s%(folder)s' % self.params

            # get all objects for this path ...
            f_obj = self.content.searchIndex.FindByInventoryPath(searchpath)
            if f_obj:
                if isinstance(f_obj, vim.Datacenter):
                    f_obj = f_obj.vmFolder
                for c_obj in f_obj.childEntity:
                    if not isinstance(c_obj, vim.VirtualMachine):
                        continue
                    if c_obj.name == name:
                        vm = c_obj
                        if self.params['name_match'] == 'first':
                            break

        return vm

    def gather_facts(self, vm):
        return gather_vm_facts(self.content, vm)

    def wait_for_tools(self, vm, poll=100, sleep=5):
        tools_running = False
        vm_facts = {}
        poll_num = 0
        vm_uuid = vm.config.uuid
        while not tools_running and poll_num <= poll:
            newvm = self.getvm(uuid=vm_uuid)
            vm_facts = self.gather_facts(newvm)
            if vm_facts['guest_tools_status'] == 'guestToolsRunning':
                tools_running = True
            else:
                time.sleep(sleep)
                poll_num += 1

        if not tools_running:
            return {'failed': True, 'msg': 'VMware tools either not present or not running after {0} seconds'.format((poll * sleep))}

        changed = False
        if poll_num > 0:
            changed = True
        return {'changed': changed, 'failed': False, 'instance': vm_facts}


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj


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
        ),
    )

    # Prepend /vm if it was missing from the folder path, also strip trailing slashes
    if not module.params['folder'].startswith('/vm') and module.params['folder'].startswith('/'):
        module.params['folder'] = '/vm%(folder)s' % module.params
    module.params['folder'] = module.params['folder'].rstrip('/')

    pyv = PyVmomiHelper(module)
    # Check if the VM exists before continuing
    vm = pyv.getvm(name=module.params['name'],
                   folder=module.params['folder'],
                   uuid=module.params['uuid'])

    # VM already exists
    if vm:
        try:
            result = pyv.wait_for_tools(vm)
            if result['failed']:
                module.fail_json(**result)
            else:
                module.exit_json(**result)
        except Exception:
            e = get_exception()
            module.fail_json(msg="Waiting for tools failed with exception: %s" % e)
    else:
        module.fail_json(msg="Unable to wait for tools for non-existing VM %(name)s" % module.params)

if __name__ == '__main__':
    main()
