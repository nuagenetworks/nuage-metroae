#!/usr/bin/python

from ansible.errors import AnsibleError
import re

# Copyright 2017 Nokia
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


def bgp_summary_to_json(string):
    ''' Given a string representation of the output of "show router bgp summary"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "BGP Admin State": "Up",
      "BGP Oper State": "Up",
      "Total Peers": "2",
      "Peers": [
        {
          "IP addr": "1.1.1.2",
          "Uptime": "01h02m03s",
          "IPV4_counts": "0/0/0",
          "evpn_counts": "0/0/31"
        },
        {
          "IP addr": "1.1.1.3",
          "Uptime": "01h02m05s",
          "IPV4_counts": "0/0/0",
          "evpn_counts": "7/0/24"
        }
      ]
    }
    '''
    IP_ADDR_COMP_REGEX = "(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    IP_ADDR_REGEX = "(?:(?:" + IP_ADDR_COMP_REGEX + "\.){3}" + IP_ADDR_COMP_REGEX + ")"
    UPTIME_REGEX = "(?:[0-2][0-9]h[0-5][0-9]m[0-5][0-9]s)"
    CONN_REGEX = "(?:" + IP_ADDR_REGEX + "(?:\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+)" + UPTIME_REGEX + ")"
    BGP_ADMIN_STATE = "BGP Admin State"
    BGP_OPER_STATE = "BGP Oper State"
    TOTAL_PEERS = "Total Peers"
    json = "{"
    scratch = string.split('\n')
    found = False
    for line in scratch:
        if BGP_ADMIN_STATE in line:
            json += "\"" + BGP_ADMIN_STATE + "\": "
            if len(line.split(':')) < 2:
                raise AnsibleError(BGP_ADMIN_STATE + ' output unexpected format')
            json += "\"" + line.split(':')[1].split()[0].strip() + "\",\n"
            found = True
            break
    if not found:
        raise AnsibleError(BGP_ADMIN_STATE + ' not found')
    found = False
    for line in scratch:
        if BGP_OPER_STATE in line:
            json += "\"" + BGP_OPER_STATE + "\": "
            if len(line.split(':')) < 3:
                raise AnsibleError(BGP_OPER_STATE + ' output unexpected format')
            json += "\"" + line.split(':')[2].strip() + "\","
            found = True
            break
    if not found:
        raise AnsibleError(BGP_OPER_STATE + ' not found')
    found = False
    for line in scratch:
        if TOTAL_PEERS in line:
            json += "\"" + TOTAL_PEERS + "\": "
            if len(line.split(':')) < 3:
                raise AnsibleError(TOTAL_PEERS + ' output unexpected format')
            json += "\"" + line.split(':')[2].strip() + "\","
            found = True
            break
    if not found:
        raise AnsibleError(TOTAL_PEERS + ' not found')
    json += "\"Peers\": ["
    if len(string.split('Neighbor')) < 2:
        raise AnsibleError('Neighbor information missing')
    connections = string.split('Neighbor')[1].strip()
    if len(re.split('-+', connections)) < 2:
        raise AnsibleError('Neighbor information unexpected format')
    connections = re.split('-+', connections)[1]
    connections = connections.replace('\n', '\t').strip()
    matches = re.findall(CONN_REGEX, connections)
    for match in matches:
        connection = match.split('\t')
        if len(connection) < 2 or len(connection[1].split()) < 4:
            raise AnsibleError('Peer information unexpected format')
        json += "{\"IP Addr\": \"" + connection[0].strip() + "\","
        json += "\"Uptime\": \"" + connection[1].split()[3].strip() + "\"}"
        if line != matches[-1]:
            json += ","
    json += "]}"
    return json


def xmpp_server_detail_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller xmpp-server detail"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "XMPP FQDN": "vsd1.example.com",
      "XMPP User Name": "vsc3",
      "State": "Functional"
    }
    '''
    XMPP_FQDN = "XMPP FQDN"
    XMPP_USER_NAME = "XMPP User Name"
    STATE = "State"
    json = "{"
    scratch = string.split('\n')
    found = False
    for line in scratch:
        if XMPP_FQDN in line:
            json += "\"" + XMPP_FQDN + "\": "
            if len(line.split()) < 4:
                raise AnsibleError(XMPP_FQDN + ' output unexpected format')
            json += "\"" + line.split()[3].strip() + "\","
            found = True
            break
    if not found:
        raise AnsibleError(XMPP_FQDN + ' not found')
    found = False
    for line in scratch:
        if XMPP_USER_NAME in line:
            json += "\"" + XMPP_USER_NAME + "\": "
            if len(line.split()) < 5:
                raise AnsibleError(XMPP_USER_NAME + ' output unexpected format')
            json += "\"" + line.split()[4].strip() + "\","
            found = True
            break
    if not found:
        raise AnsibleError(XMPP_USER_NAME + ' not found')
    found = False
    for line in scratch:
        if STATE in line:
            json += "\"" + STATE + "\": "
            if len(line.split()) < 3:
                raise AnsibleError(STATE + ' output unexpected format')
            json += "\"" + line.split()[2].strip() + "\""
            found = True
            break
    if not found:
        raise AnsibleError(STATE + ' not found')
    json += "}"
    return json


def show_vswitches_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vswitches"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "No. of virtual switches": "27"
    }
    '''
    NUMVSWITCHES = "No. of virtual switches"
    json = "{\"" + NUMVSWITCHES + "\": "
    scratch = string.split('\n')
    found = False
    for line in scratch:
        if NUMVSWITCHES in line:
            if len(line.split(':')) < 2:
                raise AnsibleError(NUMVSWITCHES + ' output unexpected format')
            json += "\"" + line.split(':')[1].strip() + "\","
            found = True
            break
    if not found:
        json += "\"0\","
    json += "}"
    return json


def show_vports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vports type vm detail"
    or "show vswitch-controller vports type host detail"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "No. of virtual ports": "12"
    }
    '''
    NUMVPORTS = "No. of virtual ports"
    json = "{\"" + NUMVPORTS + "\": "
    scratch = string.split('\n')
    found = False
    for line in scratch:
        if NUMVPORTS in line:
            if len(line.split(':')) < 2:
                raise AnsibleError(NUMVPORTS + ' output unexpected format')
            json += "\"" + line.split(':')[1].strip() + "\","
            found = True
            break
    if not found:
        json += "\"0\","
    json += "}"
    return json


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'bgp_summary_to_json': bgp_summary_to_json,
            'xmpp_server_detail_to_json': xmpp_server_detail_to_json,
            'show_vswitches_to_json': show_vswitches_to_json,
            'show_vports_to_json': show_vports_to_json
        }
