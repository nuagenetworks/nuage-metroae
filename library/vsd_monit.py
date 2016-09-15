#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: vsd_monit
short_description: Verify the summary of vsd processes via monit
options:
  name:
    description:
      - The name of the I(monit) program/process
    required: true
    default: null
  state:
    description:
      - The state of service
    required: true
    default: null
    choices: [ "summary" ]
'''

EXAMPLES = '''
# Verify the state of program "ntpd-status" state.
- monit: name=ntpd-status state=summary
'''


def main():
    arg_spec = dict(
        name=dict(required=True, type='list'),
        state=dict(required=True, choices=['summary'])
    )

    monit_stats = dict()
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    vsd_stats_proc = module.params['name']
    state = module.params['state']

    MONIT = module.get_bin_path('monit', True)

    def status(proc_name):
        """Return the status of the process in monit, or
        the empty string if not present."""
        rc, out, err = module.run_command('%s summary %s'
                                          % (MONIT, proc_name), check_rc=True)
        for line in out.split('\n'):
            parts = line.split()
            if len(parts) > 2:
                if (parts[0].lower() == 'program' or
                   parts[0].lower() == 'process'):
                    if parts[1] == "'%s'" % proc_name:
                        return ' '.join(parts[2:]).lower()
        else:
            return ''

    if state == 'summary':
        for proc_name in vsd_stats_proc:
            proc_status = status(proc_name)
            monit_stats[proc_name] = proc_status
        module.exit_json(changed=True, name=proc_name, state=monit_stats)

# Run the main

main()
