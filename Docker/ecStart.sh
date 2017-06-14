#!/bin/bash

#
# Start script for Nuage Metro container
#

function show_usage() {
 echo "Copyright (C) 2017 Nuage Networks, all rights reserved. Version 1.0 2017-06-14"
 echo "Usage: docker run -it --rm -v \`pwd\`:/files nuage/metro" 
 
 exit 0
}

if [ $# == 0 ] || [ ! -d /files ]; then
 show_usage
fi

# Generate sample 
if [ ! -f /files/build_vars.yml ]; then

# Copy sample config file to bind-mounted user dir, dont overwrite changes
cp -n nuage-metro/examples/* /files/

HOST_IP=`ip route get 8.8.8.8 | head -1 | cut -d' ' -f8`
cat > /files/build_vars.yml << EOF
nuage_zipped_files_dir: "/files"
nuage_unzipped_files_dir: "/files/nuage-unpacked"

###
# Usernames
# remote_user names for ansible to execute as on the target server (hypervisor)
# and Ansible host. target_server_username is the remote_user for all hypervisors.
# ansible_sudo_username is the sudo user for local actions.
target_server_username: "root"
ansible_sudo_username: "root"

vsd_standalone: False
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
ansible_deployment_host: 172.17.0.1
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

EOF

echo "Sample config file created as 'build_vars.yml', edit it and then re-run this tool"
exit 0
fi

# Re-generate new host key every time the script is run
ssh-keygen -h -f /root/.ssh/id_rsa -N ''

# Run Ansible playbooks
export ANSIBLE_HOST_KEY_CHECKING=False
cp /files/build_vars.yml nuage-metro/
if [ ! -d /files/nuage-unpacked ]; then
ansible-playbook nuage-metro/nuage_unzip.yml $@
fi

cd nuage-metro && \
ansible-playbook -c paramiko --ask-pass build.yml $@ && \
ansible-playbook -i hosts -c paramiko --ask-pass install_everything.yml $@

exit $?
