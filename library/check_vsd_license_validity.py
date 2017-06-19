#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
try:
    from vspk.v4_0 import NUVSDSession
    HAS_VSPK = True
except ImportError:
    HAS_VSPK = False

DOCUMENTATION = '''
---
module: check_vsd_license_validity
short_description: Check VSD License additional_supported_versions object to validate license across upgrades
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
'''

EXAMPLES = '''
# Check if new license are required after the upgrade
- check_vsd_license_validity:
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://10.0.0.10:8443
    state: enabled
'''


def check_license_mode(csproot):
    valid = True
    license_list = []

    try:
        license_list = csproot.licenses.get()
        for lic in license_list:
            if lic.additional_supported_versions == 0:
                valid = False
    except Exception as e:
        module.fail_json(msg="Could not retrieve license mode : %s" % e)
    module.exit_json(changed=False, result="%s" % valid)


def get_vsd_session(vsd_auth):
    try:
        session = NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
        return csproot
    except Exception as e:
        module.fail_json(msg="Could not establish connection to VSD %s" % e)


arg_spec = dict(vsd_auth=dict(required=True, type='dict'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    if not HAS_VSPK:
            module.fail_json(msg='vspk is required for this module')

    vsd_auth = module.params['vsd_auth']

    csproot = get_vsd_session(vsd_auth)
    check_license_mode(csproot)


# Run the main

if __name__ == '__main__':
    main()
