#!/usr/bin/python

import re
import json

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


def numeric_name_value_helper(name, delimiter, string):
    ''' Matches "name <delimiter> <numeric_value>" in the string and returns <numeric_value>
    If no match, returns 0.
    '''
    VALUE_RE = "\s*" + delimiter + "\s*(\d+)\s+"
    scratch = re.search(name + VALUE_RE, string)
    if scratch:
        return scratch.group(1)
    else:
        return "0"


def string_name_value_helper(name, delimiter, string):
    ''' Matches "name <delimiter> <text_value>" in the string and returns <text_value>
    If no match, returns "None"
    '''
    VALUE_RE = "\s*" + delimiter + "\s*(\S+)\s+"
    scratch = re.search(name + VALUE_RE, string)
    if scratch:
        return scratch.group(1)
    else:
        return "None"


def bgp_summary_to_json(string):
    ''' Given a string representation of the output of "show router bgp summary"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show router bgp summary",
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
    dict = {}
    peer_list = []
    dict["Command"] = "show router bgp summary"
    dict[BGP_ADMIN_STATE] = string_name_value_helper(BGP_ADMIN_STATE, ':', string) + ","
    dict[BGP_OPER_STATE] = string_name_value_helper(BGP_OPER_STATE, ':', string) + ","
    dict[TOTAL_PEERS] = numeric_name_value_helper(TOTAL_PEERS, ':', string) + ","
    peers = re.findall(PEER_RE, string)
    for peer in peers:
        peer_dict = {}
        peer_dict["IP Addr"] = peer[0]
        peer_dict["Uptime"] = peer[1]
        peer_dict["IPV4 counts"] = peer[2]
        peer_dict["evpn counts"] = peer[3]
        peer_list.append(peer_dict)
    dict["Peers"] = peer_list
    return json.dumps(dict)


def xmpp_server_detail_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller xmpp-server detail"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller xmpp-server detail",
      "XMPP FQDN": "vsd1.example.com",
      "XMPP User Name": "vsc3",
      "State": "Functional"
    }
    '''
    XMPP_FQDN = "XMPP FQDN"
    XMPP_USER_NAME = "XMPP User Name"
    STATE = "State"
    dict = {}
    dict["Command"] = "show vswitch-controller xmpp-server detail"
    dict[XMPP_FQDN] = string_name_value_helper(XMPP_FQDN, ':', string)
    dict[XMPP_USER_NAME] = string_name_value_helper(XMPP_USER_NAME, ':', string)
    dict[STATE] = string_name_value_helper(STATE, ':', string)
    return json.dumps(dict)


def show_vswitches_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vswitches"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller vswitches",
      "No. of virtual switches": "27",
      "Instances": [
        {
          "vswitch-instance": "va-192.168.1.117/1",
          "Personality": "VRS",
          "Uptime": "0d 03:32:51",
          "Num": "0/0/0"
        },
        {
          "vswitch-instance": "va-192.168.1.177/1",
          "Personality": "VRS_G",
          "Uptime": "0d 03:32:51",
          "Num": "0/0/0"
        }
      ]
    }
    '''
    NUMVSWITCHES = "No. of virtual switches"
    INSTANCE_RE = "(\S+)\s+(\S+)\s+(\S+d \S+:\S+:\S+)\s+(\S+)"
    dict = {}
    inst_list = []
    dict["Command"] = "show vswitch-controller vswitches"
    dict[NUMVSWITCHES] = numeric_name_value_helper(NUMVSWITCHES, ':', string)
    instances = re.findall(INSTANCE_RE, string)
    for instance in instances:
        inst_dict = {}
        inst_dict["vswitch-instance"] = instance[0]
        inst_dict["Personality"] = instance[1]
        inst_dict["Uptime"] = instance[2]
        inst_dict["Num"] = instance[3]
        inst_list.append(inst_dict)
    dict["Instances"] = inst_list
    return json.dumps(dict)


def show_host_vports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vports type host detail"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller vports type host detail",
      "No. of virtual ports": "12",
      "Vports": [
        {
          "VP Name": "va-10.15.2.254/1/1",
          "G/W PortName": "eth2",
          "VLAN ID": "11",
          "VPRN": "20159",
          "EVPN": "20162",
          "VP IP Address": "70.70.70.11/24"
        },
        {
          "VP Name": "va-10.15.33.254/1/1",
          "G/W PortName": "eth2",
          "VLAN ID": "11",
          "VPRN": "20159",
          "EVPN": "20162",
          "VP IP Address": "70.70.70.11/24"
        }
      ]
    }
    '''
    NUMVPORTS = "No. of virtual ports"
    VPORTS_RE = "(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+\.\d+\.\d+\/\d+)"
    dict = {}
    port_list = []
    dict["Command"] = "show vswitch-controller vports type host detail"
    dict[NUMVPORTS] = numeric_name_value_helper(NUMVPORTS, ':', string)
    ports = re.findall(VPORTS_RE, string)
    for port in ports:
        port_dict = {}
        port_dict["VP Name"] = port[0]
        port_dict["G/W PortName"] = port[1]
        port_dict["VLAN ID"] = port[2]
        port_dict["VPRN"] = port[3]
        port_dict["EVPN"] = port[4]
        port_dict["VP IP Address"] = port[5]
        port_list.append(port_dict)
    dict["Vports"] = port_list
    return json.dumps(dict)


def show_vm_vports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vports type vm detail"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller vports type vm detail",
      "No. of virtual ports": "12",
      "Vports": [
        {
          "VP Name": "va-10.15.2.254/1/1",
          "VM Name": "ovs-1-vm1",
          "VPRN": "20159",
          "EVPN": "20162",
          "Multicast": "Disabled",
          "VP IP Address": "70.70.70.11/24",
          "Mac Address": "00:14:51:59:09:13"
        },
        {
          "VP Name": "va-10.15.33.254/1/2",
          "VM Name": "ovs-1-vm2",
          "VPRN": "20159",
          "EVPN": "20163",
          "Multicast": "Disabled",
          "VP IP Address": "70.70.70.104/24",
          "Mac Address": "00:14:51:59:09:15"
        }
      ]
    }
    '''
    NUMVPORTS = "No. of virtual ports"
    VPORTS_RE = "(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+\/\d+)\s+(\d+:\d+:\d+:\d+:\d+:\d+)"
    dict = {}
    port_list = []
    dict["Command"] = "show vswitch-controller vports type vm detail"
    dict[NUMVPORTS] = numeric_name_value_helper(NUMVPORTS, ':', string)
    ports = re.findall(VPORTS_RE, string)
    for port in ports:
        port_dict = {}
        port_dict["VP Name"] = port[0]
        port_dict["VM Name"] = port[1]
        port_dict["VPRN"] = port[2]
        port_dict["EVPN"] = port[3]
        port_dict["Multicast"] = port[4]
        port_dict["VP IP Address"] = port[5]
        port_dict["Mac Address"] = port[6]
        port_list.append(port_dict)
    dict["Vports"] = port_list
    return json.dumps(dict)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'bgp_summary_to_json': bgp_summary_to_json,
            'xmpp_server_detail_to_json': xmpp_server_detail_to_json,
            'show_vswitches_to_json': show_vswitches_to_json,
            'show_host_vports_to_json': show_host_vports_to_json,
            'show_vm_vports_to_json': show_vm_vports_to_json
        }
