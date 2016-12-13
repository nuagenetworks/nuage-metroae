from vspk.v4_0 import NUVSDSession, NUSubnet
import yaml
import sys
from ipaddr import IPAddress
import argparse
import json


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


def create_subnet(zone):
    lst_addr = zone.subnets.get()
    lst_networks = [net.address for net in lst_addr]
    # Incerement the subnet value by 256 to create new subnet
    lst_networks.sort()
    new_sub = IPAddress(lst_networks[-1]) + 256
    if new_sub == '10.107.0.0':
        print("ERROR: Exceeded max network limit")
        sys.exit(1)
    gateway_addr = new_sub + 1
    net_name = str(new_sub).split('.')

    subnet_info = {'address': str(new_sub),
                   'gateway': str(gateway_addr),
                   'netmask': vsd_constants['netmask'],
                   'name': 'OC_JEN_CI'+net_name[2],
                   'underlay': vsd_constants['underlay'],
                   'underlayEnabled': vsd_constants['underlayEnabled'],
                   'PATEnabled': vsd_constants['PATEnabled']
                   }
    sub_obj = NUSubnet(data=subnet_info)
    zone.create_child(sub_obj)
    return (sub_obj, net_name[2])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Set path to playbook directory.")
    parser.add_argument("subnet_name", type=str, default=None, nargs='?',
                        help="VSD subnet name to delete.")
    parser.add_argument("delete_subnet", type=bool, default=False, nargs='?',
                        help="Set to True if subnet needs to delete. \
                        Default is false")
    args = parser.parse_args()

    # Get ZFB related parameters
    try:
        with open(args.playbook_dir + '/zfb.yml', 'r') as fh:
            zfb_params = yaml.load(fh)
        with open(args.playbook_dir + '/roles/ci-predeploy/vars/main.yml',
                  'r') as fo:
            vsd_constants = yaml.load(fo)
    except Exception as e:
        print("ERROR: Could not locate file: %s" % e)

    # Create a session as csp user
    try:
        session = NUVSDSession(**zfb_params['csp'])
        session.start()
        csproot = session.user
    except:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)

    # Get zone
    zone_obj = get_zone_obj(csproot, vsd_constants['org_name'],
                            vsd_constants['domain_name'])

    # Delete subnet
    del_subnet = args.delete_subnet
    if del_subnet:
        del_subnet_name = args.subnet_name
        delete_subnet(del_subnet_name, zone_obj)
        print("Deleted subnet %s from VSD" % del_subnet_name)
    else:
        # Create subnet
        network, network_str = create_subnet(zone_obj)
        sub_info = {'sub_id': network.id,
                    'net_name': network.name,
                    'vsd_net': network.address,
                    'subnet_name': 'OC_JEN_SUBNET' + network_str
                    }
        json_info = json.dumps(sub_info)
        print json_info
