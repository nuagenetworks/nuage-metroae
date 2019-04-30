#!/usr/bin/env python
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
module: download_image
short_description: Download image from glance to local machine
options:
   auth:
     description:
        - OpenStack credentials
   image_name_id:
     description:
        - Name of the image/id to download
     required: true
     default: None
   path:
     description:
        - path to download the glance image on to local machine
     required: true
     default: None
requirements: ["shade"]
'''

EXAMPLES = '''
# Download an image from glance to local machine named centos7
- download_image:
    auth:
      auth_url: http://localhost/auth/v2.0
      username: admin
      password: passme
      project_name: admin
    image_name_id: centos7
    path: /root/project/centos7.qcow2
'''


def main():

    argument_spec = openstack_full_argument_spec(
        image_name_id=dict(required=True),
        path=dict(required=True),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    if not HAS_SHADE:
        module.fail_json(msg='shade is required for this module')

    try:
        cloud = shade.openstack_cloud(**module.params)

        image = cloud.download_image(module.params['image_name_id'],
                                     output_path=module.params['path'])
        changed = True
        module.exit_json(changed=changed, image=image)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
