#!/usr/bin/python
# Copyright 2016 Nokia
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec
from ansible.module_utils.openstack import openstack_module_kwargs
try:
    import shade
    HAS_SHADE = True
except ImportError:
    HAS_SHADE = False


DOCUMENTATION = '''
---
module: create_snapshot
short_description: Create a snapshot of vm(s) in OpenStack
options:
   auth:
     description:
        - OpenStack credentials
   name:
     description:
        - Name that has to be given to the snapshot
     required: true
     default: None
   vm_id:
     description:
        - OpenStack vm instance id for which snapshot is to be created
     required: true
     default: None
requirements: ["shade"]
'''

EXAMPLES = '''
# Create snaphot for vm instance with id 788a8c96547271
- create_snapshot:
    auth:
      auth_url: http://localhost/auth/v2.0
      username: admin
      password: passme
      project_name: admin
    name: snapshot_vm1
    vm_id: 788a8c96547271
'''


def main():

    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
        vm_id=dict(required=True),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    if not HAS_SHADE:
        module.fail_json(msg='shade is required for this module')

    try:
        cloud = shade.openstack_cloud(**module.params)

        image = cloud.create_image_snapshot(name=module.params['name'],
                                            server=module.params['vm_id'],
                                            wait=True)
        changed = True
        module.exit_json(changed=changed, image=image)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
