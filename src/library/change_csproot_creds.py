#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import importlib

VSPK = None

DOCUMENTATION = '''
---
module: change_csproot_creds
short_description: Change credentials for csproot user
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
  new_pass:
    description:
      - New password for the csproot user
    required: true
    default: ""
'''

EXAMPLES = '''
# Check if new license are required after the upgrade
- check_vsd_license_validity:
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://10.0.0.10:8443
    new_pass: newpass
'''


def get_vsd_session(vsd_auth):
    # Format api version
    version = 'v5_0'
    try:
        global VSPK
        VSPK = importlib.import_module('vspk.{0:s}'.format(version))
    except ImportError:
            module.fail_json(msg='vspk is required for this module, or\
                             API version specified does not exist.')
    try:
        session = VSPK.NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
        return csproot
    except Exception as e:
        module.fail_json(msg="Could not establish connection to VSD %s" % e)


arg_spec = dict(vsd_auth=dict(required=True, type='dict'),
                new_pass=dict(required=True, type='str'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    vsd_auth = module.params['vsd_auth']
    new_pass = module.params['new_pass']

    try:
        csproot = get_vsd_session(vsd_auth)
        csproot.password = new_pass
        csproot.save()
    except Exception as e:
        module.fail_json(msg="Could not change csproot password : %s" % e)
        return

    module.exit_json(changed=False, result="%s" % "true")


# Run the main

if __name__ == '__main__':
    main()
