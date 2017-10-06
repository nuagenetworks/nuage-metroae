import re
import sys
import os.path
import argparse


# Extract bridge info from the OVS show command
def get_bridge_info(ovs_show_result):
    bridge_found = False
    controller_info = {}

    for i in range(0, len(ovs_show_result)):

        if ("Bridge \"" in ovs_show_result[i]):
            try:
                bridge = re.search('Bridge \"(.+?)\"', ovs_show_result[i]).group(1)
            except:
                bridge = 'NA'

            if (bridge == "alubr0"):
                bridge_found = True
            else:
                bridge_found = False

        if (bridge_found is True and "Controller \"" in ovs_show_result[i]):
            try:
                controller_info["controller"] = re.search('Controller \"(.+?)\"',
                                                          ovs_show_result[i]).group(1)
            except:
                controller_info["controller"] = 'NA'

            try:
                controller_info["target"] = re.search('target: \"tcp:(.+?):',
                                                      ovs_show_result[i + 1]).group(1)
            except:
                controller_info["target"] = 'NA'

            if ('role:' in ovs_show_result[i + 2]):
                controller_info["role"] = 'master' if ('master'
                                                       in ovs_show_result[i + 2]) else 'slave'
            else:
                controller_info["role"] = 'NA'

            try:
                controller_info["connected"] = re.search('is_connected: (.*)',
                                                         ovs_show_result[i + 3]).group(1)
            except:
                controller_info["connected"] = 'NA'

            yield controller_info


# Verifies results of OVS show command
def verify_ovs_result(ovs_show_result):
    not_connected_list = []

    if (not ovs_show_result):
        print ("Error! OVS show results are empty!")
        sys.exit(1)

    for controller_info in get_bridge_info(ovs_show_result):
        if (not controller_info):
            print ("Error!No controller info found in OVS show results!")
            sys.exit(1)

        if (controller_info["connected"] != 'true'):
            not_connected_list.append(" Bridge: alubr0" +
                                      " Controller:" + controller_info["controller"] +
                                      " IP Address:" + controller_info["target"] +
                                      " Role:" + controller_info["role"] +
                                      " Connected:" + controller_info["connected"])

    return not_connected_list


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
    error = ''
    parser = argparse.ArgumentParser()
    parser.add_argument("vrs_ip", type=str,
                        help="IP address of the VRS.")
    parser.add_argument("ovs_output_file", type=str,
                        help="File for output of command ovs-vsctl show.")
    args = parser.parse_args()
    ovs_output_file = args.ovs_output_file

    if (not is_valid_ip(args.vrs_ip)):
        print (" Error! Invalid input: vrs_ip.")
        sys.exit(1)

    if (not ovs_output_file):
        print ("Error! Invalid input: ovs_output_file.")
        sys.exit(1)

    vrs_ip = args.vrs_ip
    if (not os.path.exists(ovs_output_file)):
        print ("ERROR! Temporary file {0} not found." .format(ovs_output_file))
        sys.exit(1)

    try:
        with open(ovs_output_file, "r") as fp:
            ovs_show_result = fp.readlines()
    except:
        print("Error processing temporary file {0}:"
              "{1}" .format(ovs_output_file, sys.exc_info()[0]))
        sys.exit(1)

    if (not ovs_show_result):
        print ("Error! OVS show command results not found.")
        sys.exit(1)

    # Verify ovs-vsctl show command results
    error_list = verify_ovs_result(ovs_show_result)

    if (not error_list):
        result = "VRS " + vrs_ip + " is OK!"
    else:
        result = "Error! VRS " + vrs_ip + " did not detect the following controllers:" + str(error_list)

    print result
