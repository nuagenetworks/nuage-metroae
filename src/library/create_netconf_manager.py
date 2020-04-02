#!/usr/bin/env python

import vspk.v5_0 as VSPK

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''

---
module: create_netconf_manager
short_description: Creates a zero-factor bootstrap profile for NSGvs
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
      - proxy_user
    required:True
'''

EXAMPLES = '''
- create_zfb_profile:
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
        proxy_user: proxy
'''


def create_proxy_user(module, session):
    netconf_manager_user = module.params['netconf_manager_user']

    # Create proxy user if not present
    cspenterprise = VSPK.NUEnterprise()
    cspenterprise.id = session.me.enterprise_id
    csp_users = cspenterprise.users.get()
    lst_users = [usr.user_name for usr in csp_users]
    if netconf_manager_user['proxy_user'] not in lst_users:
        proxy_user = VSPK.NUUser(first_name=netconf_manager_user['firstName'],
                                 last_name=netconf_manager_user['lastName'],
                                 user_name=netconf_manager_user['proxy_user'],
                                 email=netconf_manager_user['email'],
                                 password=netconf_manager_user['password'])
        cspenterprise.create_child(proxy_user)
        csprootuser = VSPK.NUUser(id=session.me.id)
        csprootuser.fetch()
        csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                      'Netconf Manager Group'")
        csprootgroup.assign([proxy_user, csprootuser], VSPK.NUUser)


def main():
    arg_spec = dict(
        vsd_auth=dict(
            required=True,
            no_log=True,
            type='dict'),
        netconf_manager_user=dict(
            required=True,
            no_log=True,
            type='dict'))

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    vsd_auth = module.params['vsd_auth']

    # Create a session as csp user
    try:
        session = VSPK.NUVSDSession(**vsd_auth)
        session.start()
    except Exception as e:
        module.fail_json(
            msg="ERROR: Could not establish connection to VSD API "
                "using %s: %s" % (vsd_auth, str(e)))
        return

    create_proxy_user(module, session)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
