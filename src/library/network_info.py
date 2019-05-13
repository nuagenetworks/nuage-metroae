#!/usr/bin/env python

import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import b

# Copyright 2016 Nokia
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

DOCUMENTATION = '''
---
module: network_info
short_description: Gathers interfaces and their ip addr and
                   if specified their mac addr.
                   It also collects the hostname of the machine.
options:
  mac_addr:
    description:
      - A boolean value. If set to True, collects mac addr of interfaces
    required: true
'''

EXAMPLES = '''
# Get network info of a machine
- network_info:
    mac_addr: True
'''


def parse_ipv4cmd_output(ip_str):
    for ip_line in ip_str.split('\n'):
        try:
            ip_addr = re.search(r'inet\s+([0-9]+(?:\.[0-9]+){3})', ip_line)
            ip_addr = ip_addr.group(1)
            intf_name = ip_line.split()[1]
            net_info['interfaces'][intf_name] = {'ip': ip_addr}
        except:
            pass


def parse_maccmd_output(mac_str):
    for mac_line in mac_str.split('\n'):
        try:
            mac_addr = re.search(r'ether\s+((?:[0-9a-fA-F]:?){12})', mac_line)
            mac_addr = mac_addr.group(1)
            intf_name = mac_line.split()[1]
            net_info['interfaces'][intf_name[:-1]]['mac_addr'] = mac_addr
        except:
            pass


def execute_cmd(cmd):
    rc, out, err = module.run_command(cmd, check_rc=False)
    if err is None:
        err = b('')

    if out is None:
        out = b('')

    if rc != 0:
        module.fail_json(msg="command failed",
                         rc=rc,
                         cmd=cmd,
                         stdout=out,
                         stderr=err,
                         changed=False)
    return (out)


arg_spec = dict(
    mac_addr=dict(type='bool', required=True)
)
module = AnsibleModule(argument_spec=arg_spec)
net_info = {'interfaces': {}}


def main():
    collect_mac_addr = module.params['mac_addr']
    IPCMD = module.get_bin_path('ip', True)
    HOSTCMD = module.get_bin_path('hostname', True)

    ipv4_cmd = "%s -o -family inet addr" % (IPCMD)
    mac_cmd = "%s -o -family link addr" % (IPCMD)
    host_cmd = "%s -f" % (HOSTCMD)

    ip_str = execute_cmd(ipv4_cmd)
    mac_str = execute_cmd(mac_cmd)
    hostname = execute_cmd(host_cmd)

    parse_ipv4cmd_output(ip_str)
    if collect_mac_addr:
        parse_maccmd_output(mac_str)

    net_info['hostname'] = hostname.strip()
    module.exit_json(cmd=ip_str, info=net_info,
                     rawout=(ip_str, mac_str),
                     changed=True)


if __name__ == '__main__':
    main()
