#!/usr/bin/env python

import importlib
from ansible.module_utils.basic import AnsibleModule

VSPK = None

DOCUMENTATION = '''

---
module: create_netconf_manager
short_description: Create NETCONF user and attach it to NETCONF manager group on VSD
options:
  vsd_auth:
    description:
      - Credentials for accessing VSD.  Attributes:
      - username
      - password
      - enterprise
      - api_url
    required:True
  netconf_manager_user:
    description:
      - Parameters for proxy user to be configured.  Attributes:
      - firstName
      - lastName
      - email
      - password
      - netconf_user
    required:True
  vsd_version:
    description:
      - VSD version
    required: true
    default: null
'''

EXAMPLES = '''
- create_netconf_manager:
    vsd_auth:
        username: csproot
        password: csproot
        enterprise: csp
        api_url: https://localhost:8443
    netconf_manager_user:
        firstName: John
        lastName: Doe
        email: user@email.com
        password: pass
        netconf_user: proxy
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


def create_netconf_user(netconf_manager_user, session):

    # Create proxy user if not present
    cspenterprise = VSPK.NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if netconf_manager_user['netconf_user'] not in lst_users:
        netconf_user = VSPK.NUUser(first_name=netconf_manager_user['firstName'],
                                   last_name=netconf_manager_user['lastName'],
                                   user_name=netconf_manager_user['netconf_user'],
                                   email=netconf_manager_user['email'],
                                   password=netconf_manager_user['password'])
        cspenterprise.create_child(netconf_user)
        csprootuser = VSPK.NUUser(id=session.me.id)
        csprootuser.fetch()
        csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                      'Netconf Manager Group'")
        csprootgroup.assign([netconf_user, csprootuser], VSPK.NUUser)


def main():
    arg_spec = dict(
        vsd_auth=dict(
            required=True,
            no_log=True,
            type='dict'),
        netconf_manager_user=dict(
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
    netconf_manager_user = module.params['netconf_manager_user']

    try:
        session = get_vsd_session(vsd_auth, vsd_version)
    except ImportError:
        module.fail_json(msg='vspk is required for this module, or '
                         'API version specified does not exist.')
        return
    except Exception as e:
        module.fail_json(msg="Could not establish connection to VSD %s" % e)
        return

    create_netconf_user(netconf_manager_user, session)
    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
