# Copyright 2016 Nokia
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
from vspk.v4_0 import NUVSDSession, NUSubnet
from bambou import exceptions
import yaml
import sys
from ipaddr import IPAddress
import argparse
import json

# Network limit
NET_LIMIT = '10.107.0.0'
# Status of network creation
NET_CREATE = False


def get_zone_obj(csp_user, org_name='Nuage_Partition1',
                 l3_domain_name='oc-heat-test'):
    csproot = csp_user
    org = csproot.enterprises.get_first(filter="name=='%s'" % org_name)
    if org.name != org_name:
        print("ERROR: Could not find %s org in VSD" % org_name)
        sys.exit(1)
    l3_domain = org.domains.get_first(filter="name=='%s'" % l3_domain_name)
    if l3_domain.name != l3_domain_name:
        print("ERROR: Could not find %s domain in VSD" % l3_domain_name)
        sys.exit(1)
    zone = l3_domain.zones.get_first(filter="name=='%s'"
                                     % vsd_constants['zone_name'])

    return (zone)


def update_subnet_info(subnet_addr):
    new_sub = subnet_addr
    gateway_addr = new_sub + 1
    net_name = str(new_sub).split('.')
    subnet_info = {'address': str(new_sub),
                   'gateway': str(gateway_addr),
                   'netmask': vsd_constants['netmask'],
                   'name': 'OC_JEN_CI' + net_name[2],
                   'underlay': vsd_constants['underlay'],
                   'underlayEnabled': vsd_constants['underlayEnabled'],
                   'PATEnabled': vsd_constants['PATEnabled']
                   }
    sub_obj = NUSubnet(data=subnet_info)
    return (sub_obj, net_name[2])


def create_subnet(zone):
    global NET_CREATE
    lst_addr = zone.subnets.get()
    lst_networks = [IPAddress(net.address) for net in lst_addr]
    # Incerement the subnet value by 256 to create new subnet
    lst_networks.sort()
    new_sub = lst_networks[-1] + 256
    if new_sub == NET_LIMIT:
        print("ERROR: Exceeded max network limit")
        sys.exit(1)
    sub_obj, net_name = update_subnet_info(new_sub)
    while not NET_CREATE:
        try:
            zone.create_child(sub_obj)
            NET_CREATE = True
        except exceptions.BambouHTTPError as e:
            if 'Network overlaps' in e.message:
                new_sub = new_sub + 256
                sub_obj, net_name = update_subnet_info(new_sub)
            pass
    return (sub_obj, net_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Path to playbook directory.")
    args = parser.parse_args()

    # Get vsd related parameters
    try:
        with open(args.playbook_dir + '/roles/ci-predeploy/vars/main.yml',
                  'r') as fo:
            vsd_constants = yaml.load(fo)
    except Exception as e:
        print("ERROR: Could not locate file: %s" % e)

    # Create a session as csp user
    try:
        session = NUVSDSession(**vsd_constants['csp'])
        session.start()
        csproot = session.user
    except Exception as e:
        print("ERROR: Could not establish connection to VSD API: %s" % e)
        sys.exit(1)

    # Get zone
    zone_obj = get_zone_obj(csproot, vsd_constants['org_name'],
                            vsd_constants['domain_name'])

    # Create subnet
    network, network_str = create_subnet(zone_obj)
    sub_info = {'sub_id': network.id,
                'net_name': network.name,
                'vsd_net': network.address,
                'subnet_name': 'OC_JEN_SUBNET' + network_str
                }
    json_info = json.dumps(sub_info)
    print json_info
