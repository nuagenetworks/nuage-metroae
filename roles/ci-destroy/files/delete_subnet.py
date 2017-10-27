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
from vspk.v4_0 import NUVSDSession
import yaml
import sys
import argparse


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


def delete_subnet(network_name, zone):
    network = zone.subnets.get_first(filter="name=='%s'" % network_name)
    if network is None:
        print("%s network does not exist to delete" % network_name)
        sys.exit(1)
    if network.name != network_name:
        print("ERROR: Could not delete %s network on VSD or network does\
              not exist" % network_name)
        sys.exit(1)
    network.delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Path to playbook directory.")
    parser.add_argument("subnet_name", type=str, default=None,
                        help="VSD subnet name to delete.")
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

    # Delete subnet
    del_subnet_name = args.subnet_name
    delete_subnet(del_subnet_name, zone_obj)
    print("Deleted subnet %s from VSD" % del_subnet_name)
