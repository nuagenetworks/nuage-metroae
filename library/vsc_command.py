#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import logging

try:
    from netmiko import ConnectHandler
    HAS_CONNECTIONHANDLER = True
except:
    HAS_CONNECTIONHANDLER = False

DOCUMENTATION = '''
---
module: vsc_command
short_description: Execute a command on vsc and return the results
options:
  mgmt_ip:
    description:
      - The ip addr of the vsc management port
    required: true
  username:
    description:
      - The admin username on the vsc
    required: true
  password:
    description:
      - The admin password on the vsc
    required: true
  command:
    description:
      - The command to execute on the vsc
    required: true
  logging:
    description:
      - Optional boolean. When True, turn on netmiko logging.
  log_file_name:
    description:
      - Optional file name for logging. Only used when logging is True
'''

EXAMPLES = '''
- name: execute vsc command
  vsc_command:
    mgmt_ip: 192.168.122.123
    username: admin
    password: admin
    command: show vswitch-controller xmpp-server

  - name: check xmpp connectivity in a loop until 'Functional'
    vsc_command:
      command: show vswitch-controller xmpp-server | match Functional
      mgmt_ip: 192.168.122.123
      username: admin
      password: admin
      logging: True
      log_file_name: my_task.log
    register: xmpp_status
    until: xmpp_status.result.find('Functional') != -1
    retries: 6
    delay: 10
'''


def main():
    arg_spec = dict(
        mgmt_ip=dict(required=True, type='str'),
        username=dict(required=True, type='str', no_log=True),
        password=dict(required=True, type='str', no_log=True),
        command=dict(required=True, type='str'),
        logging=dict(default=False, type='bool'),
        log_file_name=dict(default='vsc_command.log', type='str')
    )

    module = AnsibleModule(argument_spec=arg_spec, supports_check_mode=True)
    if not HAS_CONNECTIONHANDLER:
        MESSAGE = "Unable to find netmiko library. Has it been installed?",
        module.fail_json(msg=MESSAGE,
                         rc=-1,
                         cmd='None',
                         stdout='None',
                         stderr=MESSAGE,
                         changed=False)

    if module.params['logging']:
        logging.basicConfig(filename=module.params['log_file_name'], level=logging.DEBUG)
        logger = logging.getLogger("netmiko")

    vsc_conn_params = {
        'device_type': 'alcatel_sros',
        'ip': module.params['mgmt_ip'],
        'username': module.params['username'],
        'password': module.params['password']
    }
    try:
        vsc_connect = ConnectHandler(**vsc_conn_params)
        output = vsc_connect.send_command(module.params['command'])
        vsc_connect.disconnect()
    except Exception as e:
        module.fail_json(msg='Failed to execute command on vsc',
                         rc=-1,
                         cmd=module.params['command'],
                         stdout=output,
                         conn='Connection: %s' % vsc_conn_params,
                         stderr='Python exception: %s' % e,
                         changed=False)

    module.exit_json(changed=True, result=output)


main()
