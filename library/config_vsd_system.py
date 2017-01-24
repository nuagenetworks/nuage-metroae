#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
try:
    from vspk.v4_0 import NUVSDSession
    HAS_VSPK = True
except ImportError:
    HAS_VSPK = False

DOCUMENTATION = '''
---
module: config_vsd_system
short_description: Update/configure VSD System parameters
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
  gateway_purge_time:
    description:
      - Increase or decrease timeout value in VSD
    required: true
    default: null
'''

EXAMPLES = '''
# Verify the state of program "ntpd-status" state.
- config_vsd_system:
    vsd_auth:
      username: csproot
      password: csproot
      enterprise: csp
      api_url: https://10.0.0.10:8443
    gateway_purge_time: 7003
'''


def get_vsd_session(vsd_auth):
    try:
        session = NUVSDSession(**vsd_auth)
        session.start()
        csproot = session.user
        return csproot
    except:
        module.exit_json(changed=False, result="Could not establish\
                          connection to VSD")


arg_spec = dict(
        vsd_auth=dict(required=True, type='dict'),
        gateway_purge_time=dict(required=True, type='int')
)
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
if not HAS_VSPK:
        module.fail_json(msg='vspk is required for this module')


def main():
    vsd_auth = module.params['vsd_auth']
    gw_purge_time = module.params['gateway_purge_time']
    csproot = get_vsd_session(vsd_auth)
    try:
        sys_config = csproot.system_configs.get_first()
        sys_config.ad_gateway_purge_time = int(gw_purge_time)
        sys_config.save()
    except Exception as e:
        module.fail_json(msg="Could not update\
                         gateway purge timer : %s" % e)

    module.exit_json(changed=True,
                     result="Gateway purge time set to %ssec" % gw_purge_time)


main()
