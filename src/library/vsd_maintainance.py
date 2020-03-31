#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import importlib
from bambou import exceptions

VSPK = None

DOCUMENTATION = '''
---
module: vsd_maintainance
short_description: Enable/Disable maintainance mode on all l3/l2 domains except domains with shared resources
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
  state:
    description:
      - The state of maintainance mode
    required: true
    default: null
    choices: [ "enabled", "disabled" ]
'''

EXAMPLES = '''
# Enable maintainance mode on all l3/l3 domains except domains with shared resources
- vsd_maintainace:
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://10.0.0.10:8443
    state: enabled
'''


def set_maintainance_mode(csproot, state):
    result_str = ''
    lst_enterprise_ids = []
    lst_enterprises = csproot.enterprises.get()
    for enterprise in lst_enterprises:
        if enterprise.name != 'Shared Infrastructure':
            lst_enterprise_ids.append(enterprise.id)
    lst_l3_domains = csproot.domains.get()
    if lst_l3_domains:
        for l3_domain in lst_l3_domains:
            if l3_domain.parent_id in lst_enterprise_ids:
                try:
                    if state == 'enabled':
                        l3_domain.maintenance_mode = 'ENABLED'
                        l3_domain.save()
                    elif state == 'disabled':
                        l3_domain.maintenance_mode = 'DISABLED'
                        l3_domain.save()
                except Exception as e:
                    if 'is reserved' not in str(e):
                        raise e
        result_str = result_str + \
            'Maintainance mode for all non shared L3 domains-%s,' % state
    else:
        result_str = result_str + ('No L3 domains found '
                                   'to %s maintainance mode,' % state)

    lst_l2_domains = csproot.l2_domains.get()
    if lst_l2_domains:
        for l2_domain in lst_l2_domains:
            if l2_domain.parent_id in lst_enterprise_ids:
                if state == 'enabled':
                    l2_domain.maintenance_mode = 'ENABLED'
                    l2_domain.save()
                elif state == 'disabled':
                    l2_domain.maintenance_mode = 'DISABLED'
                    l2_domain.save()
        result_str = result_str + \
            ' Maintainance mode for all non shared L2 domains-%s,' % state
    else:
        result_str = result_str + (' No L2 domains found '
                                   'to %s maintainance mode' % state)

    return result_str


def get_vsd_session(vsd_auth):
    # Format api version
    version = 'v5_0'

    global VSPK
    VSPK = importlib.import_module('vspk.{0:s}'.format(version))

    session = VSPK.NUVSDSession(**vsd_auth)
    session.start()
    csproot = session.user
    return csproot


def main():
    arg_spec = dict(
        vsd_auth=dict(required=True, type='dict'),
        state=dict(required=True, choices=['enabled', 'disabled'])
    )
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    vsd_auth = module.params['vsd_auth']
    state = module.params['state']

    try:
        csproot = get_vsd_session(vsd_auth)
    except ImportError:
        module.fail_json(rc=1, msg='vspk is required for this module, or '
                         'API version specified does not exist.')
        return

    except Exception as e:
        module.fail_json(rc=1,
                         msg="Could not establish connection to VSD %s" % e)
        return

    try:
        result_str = set_maintainance_mode(csproot, state)
        module.exit_json(rc=0, changed=True, result="%s" % result_str)
    except exceptions.BambouHTTPError as be:
        if "There are no attribute changes" in str(be):
            module.exit_json(rc=0, changed=True,
                             result="Maintainance mode is already enabled")
            return
        else:
            module.fail_json(rc=1,
                             msg="Could not set maintainance mode : %s" % be)
            return
    except Exception as e:
        module.fail_json(rc=1, msg="Could not set maintainance mode : %s" % e)
        return


if __name__ == '__main__':
    main()
