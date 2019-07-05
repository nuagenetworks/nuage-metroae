#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import importlib
from bambou import exceptions

VSPK = None

DOCUMENTATION = '''
---
module: set_event_log
short_description: Set the sysconfig event log age
options:
  vsd_auth:
    description:
      - VSD credentials to access VSD GUI
    required: true
    default: null
  api_version:
    description:
      - VSD version
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
    api_version: 4.0.R8
    state: enabled
'''


def set_event_log(csproot, event_log_age):
    try:
        sysconfig = csproot.system_configs.get_first()
        sysconfig.event_log_entry_max_age = event_log_age
        sysconfig.save()
        module.exit_json(changed=True, result="This rocks")

    except exceptions.BambouHTTPError as be:
        if "There are no attribute changes" in be.message:
            module.exit_json(changed=True, result="Maintainance mode is already enabled")
        else:
            module.fail_json(msg="Could not set maintainance mode : %s" % be)
    except Exception as e:
        module.fail_json(msg="Could not set maintainance mode : %s" % e)


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
    api_version=dict(required=True, type='str'),
    event_log_age=dict(required=True, type='str')
)
module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)


def main():
    vsd_auth = module.params['vsd_auth']
    event_log_age = module.params['event_log_age']
    csproot = get_vsd_session(vsd_auth)
    set_event_log(csproot, event_log_age)


# Run the main

main()
