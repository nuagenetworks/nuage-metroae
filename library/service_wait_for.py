#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import time

DOCUMENTATION = '''
---
module: service_wait_for
short_description: Wait for a service/program/process managed by monit to come to active state within a given time period
options:
  name:
    description:
      - The name of the monit program/process
    required: true
    default: null
  period:
    description:
      - time period to monitor
    required: true
    default: null
  frequency:
    description:
      - frequency of polling
    required: true
    default: null
'''

EXAMPLES = '''
# Wait for the state of program "ejabberd-status" to become ok polling every 30 seconds for 600 seconds
- service_wait_for: name=ejabberd-status period=600 frequency=30
'''


def main():
    arg_spec = dict(
        name=dict(required=True, type='list'),
        period=dict(required=True, type='int'),
        frequency=dict(required=True, type='int')
    )

    monit_stats = dict()
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    vsd_stats_proc = module.params['name']
    period = module.params['period']
    frequency = module.params['frequency']

    MONIT = module.get_bin_path('monit', True)

    def status(proc_name):
        """Return the status of the process in monit, or
        the empty string if not present."""
        rc, out, err = module.run_command('%s summary %s'
                                          % (MONIT, proc_name), check_rc=True)
        for line in out.split('\n'):
            parts = line.split()
            if len(parts) > 2:
                if parts[0].lower() == 'program':
                    if parts[1] == "'%s'" % proc_name:
                        return ' '.join(parts[2:]).lower()
                elif parts[0].lower() == 'process':
                    if parts[1] == "'%s'" % proc_name:
                        return ' '.join(parts[3:]).lower()
        else:
            return ''

    desired_state = False
    time_elapsed = 0

    for proc_name in vsd_stats_proc:
        proc_status = status(proc_name)
        while desired_state == False and time_elapsed < period:
              if proc_status == 'ok' or 'running':
                 desired_state = True
              else:
                 time.sleep(frequency)
                 time_elapsed = time_elapsed + frequency

              proc_status = status(proc_name)

        monit_stats[proc_name] = proc_status
        monit_stats["Time taken"] = time_elapsed
        monit_stats["Desired state"] = desired_state

    if desired_state == True:
        module.exit_json(changed=True, name=proc_name, state=monit_stats)
    else:
        module.fail_json(msg="Process %s did not transitioned to active within %i seconds" % (proc_name, period))
        # Run the main


main()
