from netmiko import ConnectHandler
import re
import yaml
import sys
import time
import os.path
import argparse

import logging
logging.basicConfig(filename='vsc_verify.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


# Returns lines with vsc host names
def get_vsclines(fp):
    vsc_start = False
    for line in fp:
        # Removes any whitespace before and after the line
        line = line.strip()
        if (line.startswith("[vscs]")):
            vsc_start = True

        # Start appending lines only for [vscs] group
        if (vsc_start and line and not line.startswith("#")):
            if (line.startswith("[")):
                # Reset flag to False if group name is other than vscs
                if (not line.startswith("[vscs]")):
                    vsc_start = False
            else:
                yield line


# Returns the list of VSC hosts
def get_vschosts(playbook_dir):
    fp = ''
    hosts_file = playbook_dir + '/hosts'
    vsc_host_list = []

    if (not os.path.exists(hosts_file)):
        print ("ERROR! Hosts file not found.")
        sys.exit(1)

    try:
        with open(hosts_file, 'r') as fp:
            for lines in get_vsclines(fp):
                vsc_host_list.append(lines)
    except BaseException:
        print(
            "Error processing hosts file {0}:{1}" .format(
                hosts_file,
                sys.exc_info()[0]))
        sys.exit(1)

    return vsc_host_list


# Returns a dictionary of hostvars of each vsc
def get_vscinfo(playbook_dir):
    # get vsc hostnames list
    vsc_hosts = get_vschosts(playbook_dir)
    # Extract data from each host into a dictionary list
    vsc_host_vars = {}

    for vscs in vsc_hosts:
        host_vars_path = playbook_dir + "/host_vars/" + vscs
        if (not os.path.exists(host_vars_path)):
            print (
                "ERROR! Host_vars file not found for host: {0}." .format(host_vars_path))
            sys.exit(1)

        try:
            with open(host_vars_path, "r") as stream:
                vsc_host_vars[vscs] = yaml.safe_load(stream)
        except BaseException:
            print("Error processing host_vars file {0}:"
                  "{1}" .format(host_vars_path, sys.exc_info()[0]))
            sys.exit(1)

    return vsc_host_vars


# Returns the commands to be executed
def get_commands(playbook_dir):
    command_path = playbook_dir + "/scripts/vars/commands.yml"
    if (not os.path.exists(command_path)):
        print ("ERROR! Commands.yml file not found.")
        sys.exit(1)

    try:
        with open(command_path, "r") as stream:
            commands = yaml.safe_load(stream)
    except BaseException:
        print(
            "Error processing commands file {0}:{1}" .format(
                command_path,
                sys.exc_info()[0]))
        sys.exit(1)

    return commands['vsc_commands']


# Returns result of executing commands using netmiko
def exec_command(vsc, command):
    if (not vsc or not command):
        print("Error! Bad arguments!")
        sys.exit(1)

    try:
        net_connect = ConnectHandler(**vsc)
        output = net_connect.send_command(command)
        net_connect.disconnect()
    except:
        print ("Error! Command excution failed!"
               " Command: {0} Exception: {1}" .format(command, sys.exc_info()[0]))
        sys.exit(1)

    return output


# Returns the verification status after executing all the commands
def run_commands(commands, vsc_host_vars, vsc, retry_timeout):
    error_flag = False
    result = ''
    error1 = ''
    error2 = ''

    for command in commands:
        if not command:
            break

        if (command == 'show vswitch-controller xmpp'):
            start_time = time.time()
            timeout = start_time + retry_timeout

            while ("is OK!" not in result and time.time() < timeout):
                error_flag = False
                time.sleep(5)
                # Execute command
                output = exec_command(vsc, command)
                if (re.search(r'Functional\n', output, re.I)):
                    result = "VSC " + vsc['ip'] + " is OK!"
                elif (re.search(r'Active\n', output, re.I)):
                    error_flag = True
                    error1 = "Error: VSC " + \
                        vsc['ip'] + (" XMPP connection with VSD not set.")
                else:
                    error_flag = True
                    error1 = "Error: VSC " + \
                        vsc['ip'] + (" was unable to discover VSD.")

        elif (command == 'show router bgp summary all'):
            bad_neighbor_list = []
            # Execute command
            output = exec_command(vsc, command)

            for vsc_host in vsc_host_vars:

                if (vsc_host_vars[vsc_host]['mgmt_ip'] != vsc['ip']):
                    if 'system_ip' in vsc_host_vars[vsc_host]:
                        if (re.search(
                                (vsc_host_vars[vsc_host]['system_ip'] + '\n'), output)):
                            result = "VSC " + vsc['ip'] + " is OK!"
                        else:
                            error_flag = True
                            bad_neighbor_list.append(vsc_host_vars
                                                     [vsc_host]['mgmt_ip'])
                            error2 = "Error: Missing VSC " + \
                                vsc['ip'] + (" peers:") + str(bad_neighbor_list)

        else:
            print("Error! Unexpected command!")
            sys.exit(1)

    # Set the error results if error flag is set
    if (error_flag is True):
        result = "|" + error1 + "|" + error2

    return result


# Check if IP address is valid
def is_valid_ip(ip):
    pieces = ip.split('.')
    if (len(pieces) != 4):
        return False
    try:
        return all(0 <= int(piece) < 256 for piece in pieces)
    except BaseException:
        return False

    return True


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str,
                        help="Set host IP address.")
    parser.add_argument("retry_timeout", type=float,
                        help="Set timeout to check XMPP connection stability.")
    parser.add_argument("playbook_dir", type=str,
                        help="Set path to playbook directory.")
    args = parser.parse_args()

    if (not is_valid_ip(args.ip)):
        print (" Error! Not a valid IPv4 address.")
        sys.exit(1)

    vsc = {
        'device_type': 'alcatel_sros',
        'ip': args.ip,
        'username': 'admin',
        'password': 'admin',
    }

    retry_timeout = float(args.retry_timeout)
    playbook_dir = args.playbook_dir
    if (not playbook_dir):
        print ("Error! Playbook directory not found!")
        sys.exit(1)

    # Parse commands from the yml file
    commands = get_commands(playbook_dir)
    # Get details from all VSCs for checking BGP
    vsc_host_vars = get_vscinfo(playbook_dir)

    if (not commands and not vsc_host_vars):
        print ("Error! Commands and VSC Host vars not extracted!")
        sys.exit(1)

    result = run_commands(commands, vsc_host_vars, vsc, retry_timeout)

    # Display the final results
    print ("{0}" .format(result))
