from netmiko import ConnectHandler
import yaml
import sys
import os.path
import argparse


# Returns lines with vsc host names
def get_vsclines(fp):
    vsc_lines = []
    vsc_start = False
    for line in fp:
        # Removes any whitespace before and after the line
        line = line.strip().split(" ")[0]
        if (line.startswith("[vscs]")):
            vsc_start = True

        # Start appending lines only for [vscs] group
        if (vsc_start and line):
            if (line.startswith("[")):
                # Reset flag to False if group name is other than vscs
                if (not line.startswith("[vscs]")):
                    vsc_start = False
            else:
                vsc_lines.append(line)

    yield vsc_lines


# Returns lines with vsd host names
def get_vsdlines(fp):
    vsd_lines = []
    vsd_start = False
    for line in fp:
        # Removes any whitespace before and after the line
        line = line.strip().split(" ")[0]
        if (line.startswith("[vsds]")):
            vsd_start = True

        # Start appending lines only for [vsds] group
        if (vsd_start and line):
            if (line.startswith("[")):
                # Reset flag to False if group name is other than vscs
                if (not line.startswith("[vsds]")):
                    vsd_start = False
            else:
                vsd_lines.append(line)

    yield vsd_lines


# Returns the list of VSC hosts
def get_vschosts(playbook_dir):
    fp = ''
    hosts_file = playbook_dir + '/hosts'

    if (not os.path.exists(hosts_file)):
        print ("ERROR! Hosts file not found.")
        sys.exit(1)

    try:
        with open(hosts_file, 'r') as fp:
            for lines in get_vsclines(fp):
                vsc_host_list = lines
    except:
        print("Error processing hosts file {0}:{1}"
              .format(hosts_file, sys.exc_info()[0]))
        sys.exit(1)

    return vsc_host_list


# Returns the list of VSD hosts
def get_vsdhosts(playbook_dir):
    fp = ''
    hosts_file = playbook_dir + '/hosts'

    if (not os.path.exists(hosts_file)):
        print ("ERROR! Hosts file not found.")
        sys.exit(1)

    try:
        with open(hosts_file, 'r') as fp:
            for lines in get_vsdlines(fp):
                vsd_host_list = lines
    except:
        print("Error processing hosts file {0}:{1}"
              .format(hosts_file, sys.exc_info()[0]))
        sys.exit(1)

    return vsd_host_list


# Returns a dictionary of hostvars of each vsc
def get_vscinfo(playbook_dir):
    # Get vsc hostnames list
    vsc_hosts = get_vschosts(playbook_dir)
    # Extract data from each host into a dictionary list
    vsc_host_vars = {}

    for vscs in vsc_hosts:
        host_vars_path = playbook_dir + "/host_vars/" + vscs
        if (not os.path.exists(host_vars_path)):
            print ("ERROR! Host_vars file not found for host: {0}."
                   .format(host_vars_path))
            sys.exit(1)

        try:
            with open(host_vars_path, "r") as stream:
                vsc_host_vars[vscs] = yaml.safe_load(stream)
        except:
            print("Error processing host_vars file {0}:"
                  "{1}" .format(host_vars_path, sys.exc_info()[0]))
            sys.exit(1)

    return vsc_host_vars


# Returns a dictionary of hostvars of each vsd
def get_vsdinfo(playbook_dir):
    # Get vsd hostnames list
    vsd_hosts = get_vsdhosts(playbook_dir)
    # Extract data from each host into a dictionary list
    vsd_host_vars = {}

    for vsds in vsd_hosts:
        host_vars_path = playbook_dir + "/host_vars/" + vsds
        if (not os.path.exists(host_vars_path)):
            print ("ERROR! Host_vars file not found for host: {0}."
                   .format(host_vars_path))
            sys.exit(1)

        try:
            with open(host_vars_path, "r") as stream:
                vsd_host_vars[vsds] = yaml.safe_load(stream)
        except:
            print("Error processing host_vars file {0}:"
                  "{1}" .format(host_vars_path, sys.exc_info()[0]))
            sys.exit(1)

    return vsd_host_vars


# Returns the commands to be executed
def get_commands(playbook_dir):
    command_path = playbook_dir + "/roles/vns-deploy/vars/main.yml"
    if (not os.path.exists(command_path)):
        print ("ERROR! Commands.yml file not found.")
        sys.exit(1)

    try:
        with open(command_path, "r") as stream:
            commands = yaml.safe_load(stream)
    except:
        print("Error processing commands file {0}:{1}"
              .format(command_path, sys.exc_info()[0]))
        sys.exit(1)

    return commands['vns_config_commands']


# Returns result of executing commands
def exec_command(net_connect, command):
    if (not net_connect or not command):
        print("Error! Bad arguments!")
        sys.exit(1)

    try:
        if command == 'admin save':
            try:
                output = net_connect.send_command(command, expect_string='cf1:')
            except:
                output = net_connect.send_command(command)
        else:
            output = net_connect.send_command(command)
    except:
        print ("Error! Command excution failed!" " Command: {0} Exception: {1}"
               .format(command, sys.exc_info()[0]))
        sys.exit(1)

    return output


# Returns the verification status after executing all the commands
def run_commands(commands, vsc, vsd_hosts_vars, xmpp_username):
    tls = 'configure system security tls-profile vns-tls-profile '
    tls_commands = [tls + 'own-key cf1:\%s-Key.pem' % xmpp_username,
                    tls + 'own-certificate cf1:\%s.pem' % xmpp_username,
                    tls + 'ca-certificate cf1:\%s-CA.pem' % xmpp_username]

    commands = tls_commands + commands
    try:
        net_connect = ConnectHandler(**vsc)
    except:
        print ("Error! Netmiko connection failed!" " Exception: {0}"
               .format(sys.exc_info()[0]))
        sys.exit(1)

    # Convert cmd output to dict
    for cmd in commands:
        vswitch_info = exec_command(net_connect, cmd)

    return vswitch_info


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook_dir", type=str,
                        help="Set path to playbook directory.")
    parser.add_argument("xmpp_user_name", type=str,
                        help="xmpp username")
    args = parser.parse_args()
    xmpp_username = args.xmpp_user_name

    vsc_conn = {
        'device_type': 'alcatel_sros',
        'username': 'admin',
        'password': 'admin',
    }

    playbook_dir = args.playbook_dir
    if (not playbook_dir):
        print ("Error! Playbook directory not found!")
        sys.exit(1)

    # Parse commands from the yml file
    commands = get_commands(playbook_dir)

    # Get details from all VSCs and VSDs for checking stats server info
    vsc_host_vars = get_vscinfo(playbook_dir)
    vsd_host_vars = get_vsdinfo(playbook_dir)
    if (not commands and not vsc_host_vars and not vsd_host_vars):
        print ("Error! Commands and VSC Host vars not extracted!")
        sys.exit(1)

    # Execute commads on each vsc
    for vsc in vsc_host_vars:
        vsc_conn['ip'] = vsc_host_vars[vsc]['mgmt_ip']
        result = run_commands(commands, vsc_conn, vsd_host_vars, xmpp_username)

    # Display the final results
    print ("{0}" .format(result))
