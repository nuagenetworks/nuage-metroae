from vspk.v4_0 import NUVSDSession
from datetime import datetime, timedelta
import shade
import subprocess
import argparse
import sys
import json
import yaml
import logging

# Set logging related parameters
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('ci_cleanup.log', mode='w')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)


def get_stacks(os_conn, older_than_hours, use_utc=True):
    '''
    Get the list of heat stacks from OpenStack project
    '''
    dict = {}
    stack_list = []
    stack_count_total = 0
    dict["Command"] = "openstack stack list"
    dict["Older Than Hours"] = older_than_hours
    current_time = datetime.utcnow() if use_utc else datetime.now()
    dict["Current Time"] = current_time.strftime('%Y-%m-%dT%H:%M:%S')

    try:
        stacks = os_conn.list_stacks()
    except Exception as e:
        print("ERROR: Could not get stack list from OpenStack :%s" % e)
        sys.exit(0)
    # Filter stacks based on time
    for stack in stacks:
        stack_count_total += 1
        if older_than_helper(stack['creation_time'],
                             older_than_hours, current_time):
            stack_dict = {}
            stack_dict["ID"] = stack['id']
            stack_dict["Name"] = stack['stack_name']
            stack_dict["Status"] = stack['stack_status']
            stack_dict["CreationTime"] = stack['creation_time']
            stack_dict["UpdatedTime"] = stack['updated_time']
            stack_list.append(stack_dict)
    dict["Stacks"] = stack_list
    dict["Stack Count Total"] = stack_count_total
    dict["Stack Count Filtered"] = len(stack_list)
    logger.info('Stacks info older than %s hours: \n%s' % (older_than_hours,
                                                           json.dumps(dict)))
    return (stack_list)


def delete_stacks(os_conn, stack_list):
    '''
    Given a list of stacks, this func will delete the heat stack
    from OpenStack
    '''
    # Filter ubuntu vms and delete them first
    ubuntu_stacks = [ubuntu_stack for ubuntu_stack in stack_list
                     if 'jen-slave-u' in ubuntu_stack['Name']]
    rest_of_the_stacks = [centos_stack for centos_stack in stack_list
                          if 'jen-slave-u' not in centos_stack['Name']]

    for stack in ubuntu_stacks + rest_of_the_stacks:
        logger.info("Deleting stack %s" % stack['Name'])
        try:
            os_conn.delete_stack(stack['ID'], wait=True)
        except Exception as e:
            print("ERROR: Could not delete stack from OpenStack: %s" % e)


def older_than_helper(stack_time, older_than_hours, current_time):
    '''
    Given a stack time of the form "2017-05-01T20:56:40" and
    a number of delta hours
    to check against, return True if the time is at least older_than_hours
    old. Return False if the stack_time is less than older_than_hours old.
    '''
    target_time = current_time - timedelta(hours=older_than_hours)
    stack_time_parsed = datetime.strptime(stack_time, '%Y-%m-%dT%H:%M:%S')
    if stack_time_parsed < target_time:
        return True
    return False


def get_network_details(os_conn, stack_list):
    '''
    Given a list of stack details, returns network details of the
    vm's associated with the stack name
    {'network_name': ['OC_JEN_CI_10', 'OC_JEN_CI_11'],
     'network_address': ['10.106.10', '10.106.11']
    }
    '''
    network_list = {'network_name': [],
                    'network_address': []
                    }
    for stack in stack_list:
        try:
            slave_vm = os_conn.get_stack(stack['Name'])
        except Exception as e:
            print("ERROR: Could not get stack details: %s" % e)

        # Get subnet names and extract network part from the net addr
        net_name = str(slave_vm['parameters']['network_name'])
        net_address = '.'.join(str(slave_vm['parameters']['cidr'])
                               .split('.')[0:3])
        if net_name not in network_list['network_name']:
            network_list['network_name'].append(net_name)
        if net_address not in network_list['network_address']:
            network_list['network_address'].append(net_address)
    logger.info("Network detail with subnet names and address : \n%s"
                % network_list)
    return network_list


def delete_subnets_from_vsd(net_list):
    '''
    Given a list of network subnet names, this will delete the subnets
    from the VSD using VSPK api's
    '''
    zone_obj = get_zone_obj()
    for network_name in net_list['network_name']:
        network = zone_obj.subnets.get_first(filter="name=='%s'"
                                             % network_name)
        if network is None:
            print("%s ERROR: network does not exist to delete" % network_name)
            sys.exit(1)
        if network.name != network_name:
            print("ERROR: Could not delete %s network on VSD or network does\
                  not exist" % network_name)
            sys.exit(1)
        try:
            network.delete()
        except:
            logger.error('Deleting %s subnet from VSD failed' % network.name)


def get_zone_obj():
    '''
    Read VSD credentials and get zone object from VSD
    '''
    # Get vsd related params
    with open('ci_cleanup_vars.yml', 'r') as fh:
        params = yaml.load(fh)
    # Get vsd connection
    try:
        session = NUVSDSession(**params['csp'])
        session.start()
        csproot = session.user
    except:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)

    org = csproot.enterprises.get_first(filter="name=='%s'"
                                        % params['org_name'])
    if org.name != params['org_name']:
        print("ERROR: Could not find %s org in VSD" % params['org_name'])
        sys.exit(1)
    l3_domain = org.domains.get_first(filter="name=='%s'"
                                      % params['l3_domain_name'])
    if l3_domain.name != params['l3_domain_name']:
        print("ERROR: Could not find %s domain in VSD"
              % params['l3_domain_name'])
        sys.exit(1)
    zone = l3_domain.zones.get_first(filter="name=='%s'"
                                     % params['zone_name'])

    return (zone)


def get_etc_entries(net_list):
    '''
    Given a list of network address, produce a list of entries in the
    /etc/hosts file to be deleted
    '''
    # Get /etc/hosts related params
    etc_entries = {'etc_entries': net_list['network_address']}
    return (etc_entries)


def delete_route_entries(net_list):
    '''
    Given a list of network address, delete route entries on local
    linux machine
    '''
    for net in net_list['network_address']:
        net_target = net + '.0/24'
        host1_target = net + '.3/32'
        host2_target = net + '.4/32'
        subprocess.call('sudo route del -net %s' % net_target, shell=True)
        subprocess.call('sudo route del -host %s' % host1_target, shell=True)
        subprocess.call('sudo route del -host %s' % host2_target, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("older_than_hours", type=int, default=None,
                        help="A number to query stacks older than the value.")
    args = parser.parse_args()

    # Get os related params
    with open('ci_cleanup_vars.yml', 'r') as fh:
        params = yaml.load(fh)
    try:
        conn = shade.openstack_cloud(**params['os_auth'])
    except:
        print("ERROR: Could not establish connection to OpenStack")
    stack_list = get_stacks(conn, args.older_than_hours)
    if not stack_list:
        print json.dumps({'etc_entries': []})
        logger.info('No stacks were found older than %s hours'
                    % args.older_than_hours)
        sys.exit(0)
    # Delete stacks, networks, route entries in the order
    net_details = get_network_details(conn, stack_list)
    delete_stacks(conn, stack_list)
    delete_subnets_from_vsd(net_details)
    delete_route_entries(net_details)
    print json.dumps(get_etc_entries(net_details))
