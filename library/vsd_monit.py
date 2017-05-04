#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: vsd_monit
short_description: Verify the summary of vsd processes via monit
options:
  state:
    description:
      - The state of service
    required: true
    default: null
    choices: [ "summary" ]
'''

EXAMPLES = '''
# Verify the state of vsd program/processes.
- vsd_monit: state=summary
'''


def main():
    arg_spec = dict(
        state=dict(required=True, choices=['summary'])
    )

    monit_status = dict()
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    state = module.params['state']

    MONIT = module.get_bin_path('monit', True)

    def status():
        """Return the status of the vsd process in monit, or
        the empty string if not present."""
        rc, out, err = module.run_command('%s summary'
                                          % (MONIT), check_rc=True)
        for line in out.split('\n'):
            if 'daemon' not in line:
                parts = line.split()
                if len(parts) > 2:
                    if (parts[0].lower() == 'program' or
                       parts[0].lower() == 'process' or
                       parts[0].lower() == 'file'):
                        proc_name = parts[1].strip("'")
                        proc_status = ' '.join(parts[2:]).lower()
                        monit_status.setdefault(proc_name, proc_status)
        return (monit_status)

    if state == 'summary':
        vsd_proc_status = status()
        module.exit_json(changed=True, state=vsd_proc_status)


main()
