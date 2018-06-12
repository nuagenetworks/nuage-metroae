
#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import importlib
from bambou import exceptions

VSPK = None

DOCUMENTATION = '''
---
module: vsd_addusertocmsgroup
short_description: Adds CSP user to CMS Group
options:
  vsd_auth:
    description:
      - VSD credentials for user to be added to CMS Group
    required: true
    default: null
  api_version:
    description:
      - VSD version
    required: true
    default: null


'''


def add_cspto_cms(csproot):
    try:

        cspenterprise = VSPK.NUEnterprise()
        cspenterprise.id = csproot.enterprise_id
        csp_users = cspenterprise.users.get()
        lst_users = [usr.user_name for usr in csp_users]

        csprootuser = VSPK.NUUser(id=csproot.id)
        csprootuser.fetch()
        # Add csproot user to CMS group
        csprootgroup = cspenterprise.groups.get_first(filter="name ==\
                                                      'CMS Group'")

        csprootgroup.assign([csprootuser, csprootuser], VSPK.NUUser)

    except Exception as e:
        module.fail_json(msg="Could not assign user to CMS Group: %s" % e)
    module.exit_json(changed=True)

def format_api_version(version):
    # Handle 3.2 seperately
    if version.startswith('3'):
        return ('v3_2')
    else:
        return ('v' + version[0] + '_0')


def get_vsd_session(vsd_auth):
    # Format api version
    version = format_api_version(module.params['api_version'])
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


arg_spec = dict(
    vsd_auth=dict(required=True, type='dict'),
    api_version=dict(required=True, type='str'))

module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    vsd_auth = module.params['vsd_auth']

    csproot = get_vsd_session(vsd_auth)

    add_cspto_cms(csproot)


# Run the main

main()
  
