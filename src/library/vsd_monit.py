#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: vsd_monit
short_description: Verify the summary of vsd processes via monit
options:
  group:
    description:
      - The collection of services to return
    required: true
    default: all
    choices: [ "all", "vsd-stats", "vsd-core", "vsd-common", "check" ]
'''

EXAMPLES = '''
- vsd_monit: group=vsd-stats
'''


def main():
    arg_spec = dict(
        group=dict(required=True, choices=['all', 'vsd-stats', 'vsd-core',
                                           'vsd-common', 'check'], type='str')
    )

    monit_status = dict()
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    group_name = module.params['group']
    MONIT = module.get_bin_path('monit', True)

    cmd = ''
    if group_name == 'all':
        cmd = "%s summary" % (MONIT)
    else:
        cmd = "%s summary -g %s" % (MONIT, group_name)
    rc, out, err = module.run_command(cmd, check_rc=True)

    if rc != 0:
        module.fail_json(msg="command failed",
                         rc=rc,
                         cmd=cmd,
                         stdout=out,
                         stderr=err,
                         changed=False)

    for line in out.split('\n'):
        parts = line.split()
        if len(parts) > 2:
            if (parts[0].lower() == 'program' or
               parts[0].lower() == 'process' or
               parts[0].lower() == 'file'):
                proc_name = parts[1].strip("'")
                proc_status = ' '.join(parts[2:]).lower()
                monit_status.setdefault(proc_name, proc_status)

    module.exit_json(changed=True, state=monit_status)


main()
