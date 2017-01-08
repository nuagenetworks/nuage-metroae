#!/usr/bin/python

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


def name_value_helper(name, delimiter, string):
    ''' Matches "name <delimiter> <value>" in the string and returns a JSON
    snippet of the form '"name": "value",'. Whitespace around the delimiter
    is optional.
    '''
    VALUE_RE = "\s*" + delimiter + "\s*(\S+)\s+"
    scratch = re.search(name + VALUE_RE, string)
    json = "\"" + name + "\": "
    if scratch:
        json += "\"" + scratch.group(1) + "\""
    else:
        json += "\"0\""
    return json


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
          "IPV4 counts": "0/0/1",
          "evpn counts": "0/0/31"
        },
        {
          "IP addr": "1.1.1.3",
          "Uptime": "01h02m05s",
          "IPV4 counts": "0/0/0",
          "evpn counts": "7/0/24"
        }
      ]
    }
    '''
    BGP_ADMIN_STATE = "BGP Admin State"
    BGP_OPER_STATE = "BGP Oper State"
    TOTAL_PEERS = "Total Peers"
    PEER_RE = "\s+((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+\S+\s+\S+\s+\S+\s+(\S+)\s+\S+"
    json = "{"
    json += name_value_helper(BGP_ADMIN_STATE, ':', string) + ","
    json += name_value_helper(BGP_OPER_STATE, ':', string) + ","
    json += name_value_helper(TOTAL_PEERS, ':', string) + ","
    json += "\"Peers\": ["
    peers = re.findall(PEER_RE, string)
    for peer in peers:
        json += "{\"IP Addr\": \"%s\"," % (peer[0])
        json += "\"Uptime\": \"%s\"," % (peer[1])
        json += "\"IPV4 counts\": \"%s\"," % (peer[2])
        json += "\"evpn counts\": \"%s\"}" % (peer[3])
        if peer != peers[-1]:
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
    json += name_value_helper(XMPP_FQDN, ':', string) + ","
    json += name_value_helper(XMPP_USER_NAME, ':', string) + ","
    json += name_value_helper(STATE, ':', string)
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
    json = "{" + name_value_helper(NUMVSWITCHES, ':', string)
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
    json = "{" + name_value_helper(NUMVPORTS, ':', string)
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
