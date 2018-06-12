
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
      - VSD credentials of the administrator that will be used to connect to Nuage VSD
    required: true
    default: null
  user_id:
    description: Nuage User ID of user to add to CMS Group
  api_version:
    description:
      - VSD version
    required: true
    default: null


'''


def add_user_to_cms(session, user_id):
    try:

        cspenterprise = VSPK.NUEnterprise()
        cspenterprise.id = session.user.enterprise_id

        csp_users = cspenterprise.users.get()
        if user_id not in [usr.id for usr in csp_users]:
          module.fail_json(msg="Requested user is not part of CSP Enterprise")
        
        cms_group = cspenterprise.groups.get_first(filter="name == 'CMS Group'")
        cms_users = cms_group.users.get()

        if user_id in [usr.id for usr in cms_users]:
          module.exit_json(changed=False, msg="User (id=%s) is already part of CMS Group" % user_id)
        else:
          vspk_user = VSPK.NUUser(id=user_id)
          vspk_user.fetch()
          # Add user to CMS group
          cms_group.assign(cms_users+[vspk_user], VSPK.NUUser)
          module.exit_json(changed=True, msg="User (id=%s) has been added to CMS Group" % user_id)

    except Exception as e:
        module.fail_json(msg="Could not assign user to CMS Group: %s" % e)

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
        return session
    except Exception as e:
        module.fail_json(msg="Could not establish connection to VSD %s" % e)


arg_spec = dict(
    vsd_auth=dict(required=True, type='dict'),
    api_version=dict(required=True, type='str'),
    user_id=dict(default=None, required=False, type='str'))

module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=False)


def main():
    vsd_auth = module.params['vsd_auth']

    session = get_vsd_session(vsd_auth)
    
    if 'user_id' in module.params.keys() and module.params['user_id'] is not None:
      user_id = module.params['user_id']
    else:
      user_id = session.user.id

    add_user_to_cms(session, user_id)



# Run the main

main()
  
