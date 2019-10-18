#!/usr/bin/env python

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
    PEER_RE = ("\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\S+\s+\S+\s+\S+"
               "\s+(?P<up>\S+)\s+(?P<icount>\S+)\s+\S+\s+\S+\s+\S+\s+(?P<ecount>\S+)\s+\S+")
    dict = {}
    peer_list = []
    dict["Command"] = "show router bgp summary"
    dict[BGP_ADMIN_STATE] = string_name_value_helper(BGP_ADMIN_STATE, ':', string) + ","
    dict[BGP_OPER_STATE] = string_name_value_helper(BGP_OPER_STATE, ':', string) + ","
    dict[TOTAL_PEERS] = numeric_name_value_helper(TOTAL_PEERS, ':', string) + ","
    peers = re.finditer(PEER_RE, string)
    for peer in peers:
        peer_dict = {}
        peer_dict["IP Addr"] = peer.group('ip')
        peer_dict["Uptime"] = peer.group('up')
        peer_dict["IPV4 counts"] = peer.group('icount')
        peer_dict["evpn counts"] = peer.group('ecount')
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
    INSTANCE_RE = "(?P<inst>\S+)\s+(?P<pers>\S+)\s+(?P<up>\S+d \S+:\S+:\S+)\s+(?P<num>\S+)"
    dict = {}
    inst_list = []
    dict["Command"] = "show vswitch-controller vswitches"
    dict[NUMVSWITCHES] = numeric_name_value_helper(NUMVSWITCHES, ':', string)
    instances = re.finditer(INSTANCE_RE, string)
    for instance in instances:
        inst_dict = {}
        inst_dict["vswitch-instance"] = instance.group('inst')
        inst_dict["Personality"] = instance.group('pers')
        inst_dict["Uptime"] = instance.group('up')
        inst_dict["Num"] = instance.group('num')
        inst_list.append(inst_dict)
    dict["Instances"] = inst_list
    return json.dumps(dict)


def show_host_vports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vports type host"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller vports type host",
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
    VPORTS_RE = ("(?P<vpname>\S+)\s+(?P<port>\S+)\s+(?P<vlan>\d+)\s+"
                 "(?P<vprn>\d+)\s+(?P<evpn>\d+)\s+(?P<vpip>\d+\.\d+\.\d+\.\d+\/\d+)")
    dict = {}
    port_list = []
    dict["Command"] = "show vswitch-controller vports type host"
    dict[NUMVPORTS] = numeric_name_value_helper(NUMVPORTS, ':', string)
    ports = re.finditer(VPORTS_RE, string)
    for port in ports:
        port_dict = {}
        port_dict["VP Name"] = port.group('vpname')
        port_dict["G/W PortName"] = port.group('port')
        port_dict["VLAN ID"] = port.group('vlan')
        port_dict["VPRN"] = port.group('vprn')
        port_dict["EVPN"] = port.group('evpn')
        port_dict["VP IP Address"] = port.group('vpip')
        port_list.append(port_dict)
    dict["Vports"] = port_list
    return json.dumps(dict)


def show_vm_vports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vports type vm"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller vports type vm",
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
    VPORTS_RE = ("(?P<vpname>\S+)\s+(?P<vmname>\S+)\s+(?P<vprn>\d+)\s+(?P<evpn>\d+)\s+"
                 "(?P<multi>\S+)\s+(?P<vpip>\d+\.\d+\.\d+\.\d+\/\d+)\s+(?P<mac>.*)")
    dict = {}
    port_list = []
    dict["Command"] = "show vswitch-controller vports type vm"
    dict[NUMVPORTS] = numeric_name_value_helper(NUMVPORTS, ':', string)
    ports = re.finditer(VPORTS_RE, string)
    for port in ports:
        port_dict = {}
        port_dict["VP Name"] = port.group('vpname')
        port_dict["VM Name"] = port.group('vmname')
        port_dict["VPRN"] = port.group('vprn')
        port_dict["EVPN"] = port.group('evpn')
        port_dict["Multicast"] = port.group('multi')
        port_dict["VP IP Address"] = port.group('vpip')
        port_dict["Mac Address"] = port.group('mac')
        port_list.append(port_dict)
    dict["Vports"] = port_list
    return json.dumps(dict)


def show_gateway_ports_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller gateway ports"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
      "Command": "show vswitch-controller gateway ports",
      "No. of ports": "2",
      "Ports": [
        {
          "HB VLAN Interval": "n/a",
          "VSD Role": "n/a",
          "Port Mode": "access",
          "Gateway IP/Nsg Id": "10.15.2.254",
          "Gw Role": "n/a",
          "VSD Red State": "false",
          "HB VLAN Id": "n/a",
          "Portname": "eth2",
          "Gw Red State": "false",
          "Vlan-Range": "0-4094"
        },
        {
          "HB VLAN Interval": "n/a",
          "VSD Role": "n/a",
          "Port Mode": "access",
          "Gateway IP/Nsg Id": "10.15.33.254",
          "Gw Role": "n/a",
          "VSD Red State": "false",
          "HB VLAN Id": "n/a",
          "Portname": "eth2",
          "Gw Red State": "false",
          "Vlan-Range": "0-4094"
        }
      ]
    }
    '''
    NUMPORTS = "No. of Ports"
    RE = '>\S+)\s+'
    DEL = '\s+:\s+(?P<'

    GATEIP = 'Gateway IP/Nsg Id'
    PORTNM = 'Portname'
    PORTMD = 'Port Mode'
    VSDROLE = 'VSD Role'
    GWROLE = 'Gw Role'
    VLANID = 'HB VLAN Id'
    VLANINT = 'HB VLAN Interval'
    VSDRED = 'VSD Red State'
    GWRED = 'Gw Red State'
    VLANR = 'Vlan-Range'

    items = []
    items.append((GATEIP, 'gateip'))
    items.append((PORTNM, 'portnm'))
    items.append((PORTMD, 'portmd'))
    items.append((VSDROLE, 'vsdrole'))
    items.append((GWROLE, 'gwrole'))
    items.append((VLANID, 'vlanid'))
    items.append((VLANINT, 'vlanint'))
    items.append((VSDRED, 'vsdred'))
    items.append((GWRED, 'gwred'))
    items.append((VLANR, 'vlanr'))

    myregex = ''
    for item in items:
        myregex += '%s%s%s%s' % (item[0], DEL, item[1], RE)

    dict = {}
    port_list = []
    dict["Command"] = "show vswitch-controller gateway ports"
    dict[NUMPORTS] = numeric_name_value_helper(NUMPORTS, ':', string)
    ports = re.finditer(myregex, string)
    for port in ports:
        port_dict = {}
        for item in items:
            port_dict[item[0]] = port.group(item[1])
        port_list.append(port_dict)
    dict["Ports"] = port_list
    return json.dumps(dict)


def show_bof_to_json(string):
    ''' Given a string representation of the output of "show bof"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
       "Command": "show bof",
       "image_folder": "timos",
       "mgmt_ip": "10.0.0.13",
       "primary_config": "cf1:\\config.cfg",
       "primary_image": "cf1:\\timos\\cpm.tim"
       "primary_image_unix": "/timos/cpm.tim"
    }
    '''
    dict = {}
    dict["Command"] = "show bof"
    image_re = re.compile(r'primary-image\s+(.*)')
    folder_re = re.compile(r'cf[1-3]:\\(\w+)')
    config_re = re.compile(r'primary-config\s+(.*)')
    addr_re = re.compile(r'([0-9]+(?:\.[0-9]+){3})')

    img_path = re.search(image_re, string)
    img_folder = re.search(folder_re, img_path.group(1))
    config_path = re.search(config_re, string)
    ip_addr = re.search(addr_re, string)

    primary_image = img_path.group(1)
    dict["primary_image"] = primary_image
    primary_image_unix = primary_image
    if ":" in primary_image:
        primary_image_unix = primary_image.split(":")[1]
    dict["primary_image_unix"] = primary_image_unix.replace("\\", "/")
    dict["primary_config"] = config_path.group(1)
    dict["mgmt_ip"] = ip_addr.group(1)
    dict["image_folder"] = img_folder.group(1)
    return json.dumps(dict)


def image_version_to_json(string):
    ''' Given a string representation of the output of "file version timos/cpm.tim"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
       "Command": "file version timos/cpm.tim",
       "vsc_image_version": "4.0.4"
    }
    '''
    dict = {}
    dict["Command"] = "file version timos/cpm.tim"
    version_re = re.search(r'\w+-\w+-\w+-(\d+\.\d+\.\d+)', string)
    dict["vsc_image_version"] = version_re.group(1)
    return json.dumps(dict)


def show_version_to_json(string):
    ''' Given a string representation of the output of "show version"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
       "Command": "show version",
       "vsc_version": "4.0.4"
    }
    '''
    dict = {}
    dict["Command"] = "show version"
    version_re = re.search(r'TiMOS-.*-(\d+\.\d+\.\d+)', string)
    dict["vsc_version"] = version_re.group(1)
    return json.dumps(dict)


def vsc_system_connections_to_json(string):
    ''' Given a string representation of the output of "show system connections port 5222"
    as a string, return a JSON representation of a subset of the data in that output.
    A sample of the output:
    {
       "Command": "show system connections port 5222",
       "local_ip": "10.0.0.13",
       "remote_ip": "10.0.0.42"
    }
    '''
    dict = {}
    lst_ipaddr = re.findall(r'([0-9]+(?:\.[0-9]+){3})', string)
    dict["Command"] = "show system connections port 5222"
    if len(lst_ipaddr) >=2:
      dict["local_ip"] = lst_ipaddr[0]
      dict["remote_ip"] = lst_ipaddr[1]
    return json.dumps(dict)


def vsd_detail_to_json(string):
    ''' Given a string representation of the output of "show vswitch-controller vsd detail
    as a string, return a JSON representation of a subset of the date in that output.
    A sample of the output:
    {
       "Command": "show vswitch-controller vsd detail",
       "VSD-Info": [{"vsd-user": "cna@uc-xmpp.example.com/vsd1", "status": "available"},
                    {"vsd-user": "cna@uc-xmpp.example.com/vsd2", "status": "available"},
                   ]
    }
    '''
    dict = {}
    dict["Command"] = "show vswitch-controller vsd detail"
    dict["VSD-Info"] = []
    vsd_re = re.compile(r'VSD User Name\s+:\s+(?P<vsduser>(.*))\s+Uptime.*\s+Status\s+:\s+(?P<status>(\w+))')
    vsd_details = re.finditer(vsd_re, string)
    for vsd in vsd_details:
        vsd_dict = {"vsd_username": vsd.group('vsduser'),
                    "status": vsd.group('status')
                    }
        dict["VSD-Info"].append(vsd_dict)
    return json.dumps(dict)


def vsc_router_interfaces_to_json(string):
    ''' Given a string representation of the output of "show router interface" command, return
    a JSON representation of the relevant statuses of the interfaces.

    Sample output from the command as a string:
    ===============================================================================
    Interface Table (Router: Base)
    ===============================================================================
    Interface-Name                   Adm         Opr(v4/v6)  Mode    Port/SapId
       IP-Address                                                    PfxState
    -------------------------------------------------------------------------------
    control                          Up          Up/Down     Network A/2:0
       10.106.100.202/24                                            n/a
    system                           Up          Up/Down     Network system
       1.1.1.2/32                                                   n/a
    -------------------------------------------------------------------------------
    Interfaces : 2
    ===============================================================================

    Sample output after applying filter:
    "show_router_interfaces_json": {
        "control_Adm": "Up",
        "control_Oprv4": "Up",
        "control_Oprv6": "Down",
        "system_Adm": "Up",
        "system_Oprv4": "Up",
        "system_Oprv6": "Down"
    }
    '''
    dict = {}
    rows = string.split('\n')
    for row in rows:
        columns = row.split()
        if columns[0] == 'control':
            control_Adm = columns[1]
            control_Opr = columns[2].split('/')
            control_Oprv4 = control_Opr[0]
            control_Oprv6 = control_Opr[1]
        elif columns[0] == 'system':
            system_Adm = columns[1]
            system_Opr = columns[2].split('/')
            system_Oprv4 = system_Opr[0]
            system_Oprv6 = system_Opr[1]

    dict["control_Adm"] = control_Adm
    dict["control_Oprv4"] = control_Oprv4
    dict["control_Oprv6"] = control_Oprv6
    dict["system_Adm"] = system_Adm
    dict["system_Oprv4"] = system_Oprv4
    dict["system_Oprv6"] = system_Oprv6

    return json.dumps(dict)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'bgp_summary_to_json': bgp_summary_to_json,
            'xmpp_server_detail_to_json': xmpp_server_detail_to_json,
            'show_vswitches_to_json': show_vswitches_to_json,
            'show_host_vports_to_json': show_host_vports_to_json,
            'show_vm_vports_to_json': show_vm_vports_to_json,
            'show_gateway_ports_to_json': show_gateway_ports_to_json,
            'show_bof_to_json': show_bof_to_json,
            'image_version_to_json': image_version_to_json,
            'show_version_to_json': show_version_to_json,
            'vsc_system_connections_to_json': vsc_system_connections_to_json,
            'vsd_detail_to_json': vsd_detail_to_json,
            'vsc_router_interfaces_to_json': vsc_router_interfaces_to_json
        }
