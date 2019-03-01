#!/usr/bin/python

from vspk.v5_0 import NULicense, NUVSDSession
import sys

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: apply_vsd_license
short_description: Applies the VSD license after installing VSD software
options:
  vsd_license_file:
    description:
      - Set path to VSD license file
    required:True
  vsd_auth:
    description:
      - Credentials for accessing VSD.  Attributes:
      - username
      - password
      - enterprise
      - api_url
    required:True

'''

EXAMPLES = '''
- apply_vsd_license:
    vsd_license_file: /data/vsd_license.txt
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://localhost:8443
'''

def install_license(csproot, vsd_license):
    # Push the license
    test_license = NULicense(license=vsd_license)
    csproot.create_child(test_license)


def is_license_already_installed(csproot, vsd_license):
    license_unique_id = get_license_unique_id(vsd_license)

    installed_licenses = csproot.licenses.get()
    for lic in installed_licenses:
        if lic.unique_license_identifier == license_unique_id:
            return True

    return False


def get_license_unique_id(vsd_license):
    stripped = vsd_license.strip()
    return unicode(stripped[0:16] + stripped[-16:])


def main():
    vsd_license_file = module.params['vsd_license_file']
    vsd_auth = module.params['vsd_auth']

    # Get VSD license
    vsd_license = ""
    try:
        with open(vsd_license_file, 'r') as lf:
            vsd_license = lf.read()
    except Exception as e:
        module.fail_json(msg="ERROR: Failure reading file: %s" % e)
        sys.exit(1)

    # Create a session as csp user
    try:
        session = NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
    except Exception as e:
        module.fail_json(
            msg="ERROR: Could not establish connection to VSD API "
                "using %s: %s" % (vsd_auth, str(e)))
        sys.exit(1)
    try:
        if (not is_license_already_installed(csproot, vsd_license)):
            install_license(csproot, vsd_license)
    except Exception as e:
        module.fail_json(
            msg="ERROR: Could not install license/could not verify if license is already installed: %s" % (str(e)))
        sys.exit(1)

    module.exit_json(changed=True)

arg_spec = dict(
    vsd_license_file=dict(
        required=True,
        type='str'),
    vsd_auth=dict(
        required=True,
        no_log=True,
        type='dict'))

module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

if __name__ == '__main__':
    main()
