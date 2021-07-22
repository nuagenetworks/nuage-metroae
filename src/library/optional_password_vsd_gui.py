#!/usr/bin/env python

import importlib
from ansible.module_utils.basic import AnsibleModule

VSPK = None

DOCUMENTATION = '''

---
module: optional_password_vsd_gui
short_description:  Adding an option to provide an optional VSD GUI password
options:
  vsd_auth:
    description:
      - Credentials for accessing VSD.  Attributes:
      - username
      - password
      - enterprise
      - api_url
    required:True
  vsd_version:
    description:
      - VSD version
    required: true
    default: null
'''

EXAMPLES = '''
- optional_password_vsd_gui:
    vsd_auth:
        username: csproot
        password: csproot
        enterprise: csp
        api_url: https://localhost:8443
    vsd_version: 5.4.1
'''


def format_api_version(version):
    if version.startswith('5'):
        return ('v5_0')
    else:
        return ('v6')


def get_vsd_session(vsd_auth, vsd_version):
    version = format_api_version(vsd_version)
    global VSPK
    VSPK = importlib.import_module('vspk.{0:s}'.format(version))
    session = VSPK.NUVSDSession(**vsd_auth)
    session.start()
    return session


def change_password(session):

    # Create proxy user if not present
    session_user = session.user
    csprootuser = VSPK.NUUser(id=session_user.id)
    csprootuser.fetch()
    csprootuser.password = 'rootcaso'
    csprootuser.save()


def main():
    arg_spec = dict(
        vsd_auth=dict(
            required=True,
            no_log=True,
            type='dict'),
        vsd_version=dict(
            required=True,
            type='str')
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    vsd_auth = module.params['vsd_auth']
    vsd_version = module.params['vsd_version']

    try:
        session = get_vsd_session(vsd_auth, vsd_version)
    except ImportError:
        module.fail_json(msg='vspk is required for this module, or '
                         'API version specified does not exist.')
        return
    except Exception as e:
        module.fail_json(msg="Could not establish connection to VSD %s" % e)
        return

    change_password(session)
    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
