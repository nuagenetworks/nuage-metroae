#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import time

DOCUMENTATION = '''
---
module: monit_waitfor_service
short_description: Wait for a service/program/process managed by monit to come to active state within a given time timeout_seconds
options:
  name:
    description:
      - The name of the monit program/process
    required: true
    default: null
  timeout_seconds:
    description:
      - time timeout_seconds to monitor
    required: true
    default: null
  test_interval_seconds:
    description:
      - test_interval_seconds of polling
    required: true
    default: null
'''

EXAMPLES = '''
# Wait for the state of program "ejabberd-status" to become ok polling every 30 seconds for 600 seconds
- monit_waitfor_service: name=ejabberd-status timeout_seconds=600 test_interval_seconds=30
'''


def main():
    arg_spec = dict(
        name=dict(required=True, type='list'),
        timeout_seconds=dict(required=True, type='int'),
        test_interval_seconds=dict(required=True, type='int')
    )

    monit_stats = dict()
    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)

    vsd_stats_proc = module.params['name']
    timeout_seconds = module.params['timeout_seconds']
    test_interval_seconds = module.params['test_interval_seconds']

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
                        return ' '.join(parts[2:]).lower()
                elif parts[0].lower() == 'file':
                    if parts[1] == "'%s'" % proc_name:
                        return ' '.join(parts[2:]).lower()
        else:
            return ''

    desired_state = False
    time_elapsed = 0
    restarted = False

    for proc_name in vsd_stats_proc:
        proc_status = status(proc_name)
        while not desired_state and time_elapsed < timeout_seconds:
            if proc_status == 'status ok' or \
               proc_status == 'running' or \
               proc_status == 'accessible' or \
               proc_status == 'not monitored':
                    desired_state = True
            else:
                if proc_status == 'failed' and not restarted:
                    restarted = True
                    module.run_command('%s restart %s'
                                       % (MONIT, proc_name), check_rc=True)
                time.sleep(test_interval_seconds)
                time_elapsed = time_elapsed + test_interval_seconds
                proc_status = status(proc_name)

        monit_stats[proc_name] = proc_status
        monit_stats["Time taken"] = time_elapsed
        monit_stats["Desired state"] = desired_state

    if desired_state:
        module.exit_json(changed=True, name=proc_name, state=monit_stats)
    else:
        module.fail_json(msg="Process %s did not transition to active within %i seconds" % (proc_name, timeout_seconds))


if __name__ == '__main__':
    main()
