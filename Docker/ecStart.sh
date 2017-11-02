#!/bin/bash

#
# Start script for Nuage Metro container
#

function show_usage() {
 echo "Copyright (C) 2017 Nuage Networks, all rights reserved. Version 1.0 2017-06-14"
 echo "Usage: docker run -it --rm -v \`pwd\`:/files nuage/metro" 
 echo "  add 'destroy' to remove everything"
 echo "  tip: You can add '--dns:x.x.x.x' to specify a DNS server for the Ansible host (this container) to use"
 echo "  You may have to 'ssh-copy-id -i id_rsa user@target_server' to the target servers"
 echo "  To deploy a subset of servers, you can add '--limit=vstats' ( or vsds, vscs, etc. ) at the end"
 
 exit 0
}

if [ $# == 0 ] || [ ! -d /files ]; then
 show_usage
fi

# Always copy Ansible scripts, such that users can customize if needed
cp -Rn nuage-metro /files

# Generate sample 
if [ ! -f /files/build_vars.yml ]; then

cat > /files/metro_vsp_minimal_build_vars.yml << EOF
nuage_zipped_files_dir: "/files"
nuage_unzipped_files_dir: "/files/nuage-unpacked"

###
# Usernames
# remote_user names for ansible to execute as on the target server (hypervisor)
# and Ansible host. target_server_username is the remote_user for all hypervisors.
# ansible_sudo_username is the sudo user for local actions.
target_server_username: "root"
ansible_sudo_username: "root"

# Deploy everything on a single host, use it as default gateway and a VRS
target_server_global: 10.0.0.10

mgmt_net_global: 10.0.0
mgmt_netmask_global: 255.255.255.0

dns_server_list:
  - 10.0.0.4
  - 10.0.0.5
  
dns_domain: example.com

ntp_server_list:
  - 10.0.0.2
  - 10.0.0.3

vsd_sa_or_ha: sa
vsd_fqdn_global: vsd1.example.com
vsd_operations_list:
  - install
myvsds:
  - { hostname: vsd1.{{ dns_domain }},
      target_server_type: "kvm",
      target_server: "{{ target_server_global }}",
      mgmt_ip: "{{ mgmt_net_global }}.10",
      mgmt_gateway: "{{ target_server_global }}",
      mgmt_netmask: "{{ mgmt_netmask_global }}" }

vsc_operations_list:
  - install
myvscs:
  - { hostname: vsc1.{{ dns_domain }},
      target_server_type: "kvm",
      target_server: "{{ target_server_global }}",
      mgmt_ip: "{{ mgmt_net_global }}.13",
      mgmt_gateway: "{{ target_server_global }}",
      mgmt_netmask_prefix: 24,
      ctrl_ip: 192.168.0.13,
      ctrl_netmask_prefix: 24,
      ctrl_gateway: 192.168.0.1,
      vsd_fqdn: "{{ vsd_fqdn_global }}",
      system_ip: 1.1.1.1,
      xmpp_username: vsc,
      vsc_static_route_list: { 0.0.0.0/1,128.0.0.0/1 } }

vrs_operations_list:
  - install
dockermon_install: false
myvrss:
  - { vrs_set_name: vrs_set_lab,
      vrs_os_type: el7,
      avrs: False,
      active_controller_ip: 192.168.0.13,
      standby_controller_ip: 0.0.0.0,
      vrs_ip_list: [ "{{ target_server_global }}" ] }
  
ansible_deployment_host: 127.0.0.1
mgmt_bridge: "br0"
data_bridge: "br1"
images_path: "/var/lib/libvirt/images/"

## yum_proxy: http://xxxx
## yum_update: no

EOF

cat > /files/metro_vsp_cluster_build_vars.yml << EOF
nuage_zipped_files_dir: "/files"
nuage_unzipped_files_dir: "/files/nuage-unpacked"

###
# Usernames
# remote_user names for ansible to execute as on the target server (hypervisor)
# and Ansible host. target_server_username is the remote_user for all hypervisors.
# ansible_sudo_username is the sudo user for local actions.
target_server_username: "root"
ansible_sudo_username: "root"

vsd_sa_or_ha: ha
vsd_fqdn_global: xmpp.example.com
vsd_operations_list:
  - install
myvsds:
  - { hostname: vsd1.example.com,
      target_server_type: "kvm",
      target_server: 10.0.0.10,
      mgmt_ip: 192.168.0.10,
      mgmt_gateway: 192.168.0.1,
      mgmt_netmask: 255.255.255.0 }
  - { hostname: vsd2.example.com,
      target_server_type: "kvm",
      target_server: 10.0.0.11,
      mgmt_ip: 192.168.0.11,
      mgmt_gateway: 192.168.0.1,
      mgmt_netmask: 255.255.255.0 }
  - { hostname: vsd3.example.com,
      target_server_type: "kvm",
      target_server: 10.0.0.12,
      mgmt_ip: 192.168.0.12,
      mgmt_gateway: 192.168.0.1,
      mgmt_netmask: 255.255.255.0 }
ansible_deployment_host: 127.0.0.1
mgmt_bridge: "br0"
data_bridge: "br1"
images_path: "/var/lib/libvirt/images/"
ntp_server_list:
  - 10.0.0.2
  - 10.0.0.3
dns_server_list:
  - 10.0.0.4
  - 10.0.0.5
dns_domain: example.com

## yum_proxy: http://xxxx
## yum_update: no

EOF

echo "Sample config file created as '*build_vars.yml', copy one, edit it and then re-run this tool"
exit 0
fi

# Generate new host key if needed
mkdir -p --mode=700 ~/.ssh 
if [ ! -e /files/id_rsa ]; then
  ssh-keygen -h -f /files/id_rsa -N ''
fi

# Always re-copy, even if already done
# ssh-copy-id -i /files/id_rsa.pub root@127.0.0.1 || exit 1
cp /files/id_rsa* ~/.ssh/ && chmod 600 ~/.ssh/id_rsa*

# Run Ansible playbooks
export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_CONFIG=/files/ansible.cfg
cp /files/build_vars.yml /files/nuage-metro/

if [ "$1" == "destroy" ]; then
  cd /files/nuage-metro && \
  ansible-playbook --key-file=/files/id_rsa build.yml && \
  ansible-playbook -i hosts --key-file=/files/id_rsa destroy_everything.yml
  exit $?
fi

if [ ! -d /files/nuage-unpacked ] || [ "$1" == "unpack" ]; then
ansible-playbook /files/nuage-metro/nuage_unzip.yml $@
fi

cd /files/nuage-metro && \
ansible-playbook --key-file=/files/id_rsa build.yml && \
ansible-playbook -i hosts --key-file=/files/id_rsa install_everything.yml $@

exit $?
