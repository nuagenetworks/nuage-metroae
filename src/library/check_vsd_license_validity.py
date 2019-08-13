#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import importlib
import time

VSPK = None

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
  required_days_left:
    description:
      - Required number of days left before license expiration (-1 for no check)
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
    required_days_left: 365
'''


def get_licenses(csproot):
    return csproot.licenses.get()


def check_licenses_mode(licenses):
    valid = False
    for lic in licenses:
        if lic.additional_supported_versions == 0:
            valid = False

    return valid


def check_licenses_expiration(licenses, required_days_left):
    if required_days_left >= 0:
        SECONDS_PER_DAY = 60 * 60 * 24
        current_seconds = int(time.time())
        for lic in licenses:
            license_expire_seconds = int(lic.expiry_timestamp / 1000)
            seconds_left = license_expire_seconds - current_seconds

            if seconds_left < 0:
                raise Exception("VSD License has expired")

            days_left = int(seconds_left / SECONDS_PER_DAY)

            if days_left < required_days_left:
                raise Exception("VSD License will expire in %d days" %
                                days_left)


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
                required_days_left=dict(required=True, type='int'))
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    vsd_auth = module.params['vsd_auth']
    required_days_left = module.params['required_days_left']

    valid = False

    try:
        csproot = get_vsd_session(vsd_auth)
        licenses = get_licenses(csproot)
        try:
            check_licenses_expiration(licenses, required_days_left)
        except Exception as e:
            module.fail_json(msg=str(e))
            return
        valid = check_licenses_mode(licenses)
    except Exception as e:
        module.fail_json(msg="Could not retrieve licenses : %s" % e)
        return

    module.exit_json(changed=False, result="%s" % valid)


# Run the main

if __name__ == '__main__':
    main()
