from netmiko import ConnectHandler
import re
import yaml
import sys
import os.path
import argparse


# Returns result of executing commands using netmiko
def exec_command(vsc, command):
    if (not vsc or not command):
        print("Error! Bad arguments!")
        sys.exit(1)

    try:
        net_connect = ConnectHandler(**vsc)
        output = net_connect.send_command(command)
    except:
        print ("Error! Command excution failed!"
               " Command: {0} Exception: {1}" .format(command, sys.exc_info()[0]))
        sys.exit(1)

    return output


# Returns the verification status after executing all the commands
def run_commands(commands, vscs, vrs_ip):
    error_flag = False
    result = ''

    for command in commands:
        if not command:
            break

        if (command == 'show vswitch-controller vswitches'):
            # Execute command
            for vsc in vscs:
                if (not vsc):
                    print ("Error! VSC IP not found!")
                    sys.exit(1)

                netmiko_vsc = {
                    'device_type': 'alcatel_sros',
                    'ip':   vsc,
                    'username': 'admin',
                    'password': 'admin',
                }
                output = exec_command(netmiko_vsc, command)
                if (re.search(r'[^0-9]'+vrs_ip+'[^0-9]', output)):
                    result = "VRS "+vrs_ip+" is OK!"
                else:
                    error_flag = True
                    error = "Error: VSC "+vsc+" did not detect the VRS: "+vrs_ip+"!"

        else:
            print("Error! Unexpected command!")
            sys.exit(1)

    # Set the error results if error flag is set
    if (error_flag is True):
        result = "|"+error+"|"

    return result


# Returns the commands to be executed
def get_commands(playbook_dir):
    command_path = playbook_dir + "/scripts/vars/commands.yml"
    if (not os.path.exists(command_path)):
        print ("ERROR! Commands.yml file not found.")
        sys.exit(1)

    try:
        with open(command_path, "r") as stream:
            commands = yaml.safe_load(stream)
    except:
        print("Error processing commands file {0}:{1}" .format(command_path, sys.exc_info()[0]))
        sys.exit(1)

    return commands['vrs_commands']


# Check if IP address is valid
def is_valid_ip(ip):
    pieces = ip.split('.')
    if (len(pieces) != 4):
        return False
    try:
        return all(0 <= int(piece) < 256 for piece in pieces)
    except:
        return False

    return True


# Main
if __name__ == '__main__':
    ovs_show_result = ''
    parser = argparse.ArgumentParser()
    parser.add_argument("vrs_ip", type=str,
                        help="IP address of the VRS.")
    parser.add_argument("vscs", nargs=2, type=str,
                        help="IP addresses of active and standby controllers.")
    parser.add_argument("playbook_dir", type=str,
                        help="Path of playbook directory.")
    parser.add_argument("ovs_show_result", type=str,
                        help="Verification output of ovs-vsctl show command.")
    args = parser.parse_args()

    if (not is_valid_ip(args.vrs_ip)):
        print (" Error! Invalid input: vrs_ip.")
        sys.exit(1)

    if (not is_valid_ip(args.vscs[0])):
        print (" Error! Invalid input: active_vsc_ip.")
        sys.exit(1)

    if (not is_valid_ip(args.vscs[1])):
        print (" Error! Invalid input: standby_vsc_ip.")
        sys.exit(1)

    playbook_dir = args.playbook_dir

    if (not playbook_dir):
        print ("Error! Invalid input: playbook_dir.")
        sys.exit(1)

    # Parse commands from the commands file
    commands = get_commands(playbook_dir)

    if (not commands):
        print ("Error! No commands found.")
        sys.exit(1)

    result = run_commands(commands, args.vscs, args.vrs_ip)

    # Check results of ovs-vsctl show command
    ovs_show_result = args.ovs_show_result
    if (not ovs_show_result):
        print ("Error! OVS show command results not found!")
        sys.exit(1)

    if ("is OK!" not in ovs_show_result):
        if ("is OK!" not in result):
            result += "|"+ovs_show_result
        else:
            result = ovs_show_result

    # Display the final results
    print ("{0}" .format(result))
