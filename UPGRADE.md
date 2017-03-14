# Metro: Automated Upgrade of Nuage Software

## Current support for upgrade

1. As of this writing only VSD and VSC upgrade is supported
2. Supported upgrade path
   (i) 3.2.R10 to 4.0.R7

## Overview

These are the following playbooks/roles supported by metro for upgrade.

1. vsd_health.yml
2. vsd_decluster.yml
3. vsd_upgrade.yml
4. vsc_health.yml
5. vsc_backup.yml
6. vsc_upgrade.yml
7. vsp_upgrade.yml

## Details

### vsd_health.yml

This playbook/role is used to gather network and monit information of vsd(s) prior/post upgrade process. A report file with network and monit information is created (filename can be configured inside the vsd_health.yml playbook) inside reports folder. 

### vsd_decluster.yml

This palybook is a collection three individual playbooks/roles that help in making database backup, decoupling existing vsd cluster setup and gracefully stopping vsd processes. The user is expected to mount the migration scritps in respective vsd(s).

a. vsd_dbbackup.yml: This playbook/role makes vsd database backup and stores it on ansible deployment host, which is later used for spinning up new vsd(s)
b. vsd_decouple.yml: This playbook/role executes decouple script and checks for client connections
c. stop_vsd_services.yml: This playbook/role stops all vsd services on vsd(s) gracefully

### vsd_upgrade.yml

This playbook/role destroy the exsitng vsd vm(s) and boots a new vsd vm(s) with backup database. It is recommended for user to take snapshot of the old vsd vm(s) before the upgrade as they are destroyed. Current VSD upgrade supports only clustered setup.

The playbook can be configured with interested vsd(s).
e.g. 
If user is interested in upgrading vsd node1, hosts can be defined as below
- hosts: vsd_ha_node1
If user is interested in upgrading vsd node1 and node3, hosts can be defined as below
- hosts: vsd_ha_node1:vsd_ha_node3
To upgrade all vsd nodes
- hosts: vsds

### vsc_health.yml

This  playbook/role is used to gather operational information of vsc(s) prior/post upgrade process. A report file with the operational output is created (filename can be configured inside the vsc_health.yml playbook) inside reports folder.

### vsc_backup.yml

This playbook/role is used to make backup of exsiting vsc configuration, bof configuration and .tim file and copy them to ansible deployment host. These are used in case a rollback is needed.

### vsc_upgrade.yml

This playbook/role is used to upgrade vsc to new versions by copying new .tim file to the existing vsc(s) and rebooting them.

The playbook can be configured with interested vsc(s)
e.g. 
If user is interested in upgrading vsc node1, hosts can be defined as below
- hosts: vsc_ha_node1
If user is interested in upgrading vsc node1 and node2, hosts can be defined as below
- hosts: vsc_ha_node1:vsc_ha_node2
To upgrade all vsc nodes
- hosts: vscs

### vsp_upgrade.yml

All the above playbooks are captured inside a single playbook `vsp_upgrade.yml`. This playbook follows the instructions and the order of upgrading nuage components as specified in VCS install guide.

# build and reset-build playbooks

Refer `BUILD.md` build and reset-build playbooks section for more details

# nuage_unpack playbook

Refer `BUILD.md` nuage_unpack playbook section for more details

# Reference

For reference, here is a description of the contents of the `build_vars.yml` file, with comments:

```
#    # The directory where the Nuage Networks binariy archives are located. This is only
#    # required for the `nuage_unpack.yml` playbook.
#    nuage_packed_src_path: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where to extract the relevant Nuage Networks binaries to
#    nuage_unpacked_dest_path: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Parameter used to define the Hypervisor-Architecture (One of: el6|el7|ubuntu)
#    nuage_target_architecture: "el7"
#    # Parameter to define the remote sudo username to use on target servers, e.g. hypevisors.
#    target_server_username: "root"
#    # Parameter to define the sudo username to use on the ansible server.
#    ansible_sudo_username: "root"
#    # Parameter to determine major or minor upgrade. When set to false, it is considered as major upgrade
#    # minor_upgrade: "True"
#    VSD
#    # When True or undefined, all VSDs will be configured stand-alone. When False
#    # we will expect 3 VSD definitions, below, for clustered deployment.
#    vsd_standalone: True
#    # A dictionary of params for 0 or more VSDs
#    # Note: Multiple VSDs can be deployed from the same qcow2 file
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vsd1.example.com,
#          # The target server type where this VSD instance will run. Possible values: kvm
#          target_server_type: kvm,
#          # The hypervior target where this VSD instance will be run
#          target_server: 135.227.181.232,
#          # The IP address of this VSD instance
#          mgmt_ip: 192.168.122.201,
#          # The gateway IP address of this VSD instance
#          mgmt_gateway: 192.168.122.1,
#          # The netmask of this VSD instance
#          mgmt_netmask: 255.255.255.0 }
#
#
#    VSC
#    # A dictionary of params for 0 or more VSCs
#    # Note: Multiple VSCs can be deployed from the same qcow2 file
#    myvscs:
#      - { hostname: vsc1.example.com,
#          # The target server type where this VSC instance will run. Possible values: kvm
#          target_server_type: kvm,
#          # The hypervior target where this VSC instance will be run
#          target_server: 135.227.181.232,
#          # The IP address of this VSC instance
#          mgmt_ip: 192.168.122.202,
#          # The gateway IP address of this VSC instance
#          mgmt_gateway: 192.168.122.1,
#          # The netmask prefix of this VSC instance
#          mgmt_netmask_prefix: 24,
#          # The IP address for the control network of this VSC instance
#          ctrl_ip: 192.168.100.201,
#          # The netmask prefix for the control network of this VSC instance
#          ctrl_netmask_prefix: 24,
#          # The FQDN of the VSD this VSC should conect to
#          vsd_fqdn: vsd1.example.com,
#          # The system IP address and name for this VSC instance
#          system_ip: 1.1.1.2,
#          # The XMPP user name for login to VSD
#          xmpp_username: vsc,
#          # One or more static route to be configured on this VSC
#          vsc_static_route_list: { 0.0.0.0/1 } }
#      - { hostname: vsc2.example.com,
#          # The target server type where this VSC instance will run. Possible values: kvm
#          target_server_type: kvm,
#          target_server: 135.227.181.232,
#          mgmt_ip: 192.168.122.203,
#          mgmt_gateway: 192.168.122.1,
#          mgmt_netmask_prefix: 24,
#          ctrl_ip: 192.168.100.202,
#          ctrl_netmask_prefix: 24,
#          vsd_fqdn: vsd1.example.com,
#          system_ip: 1.1.1.3,
#          xmpp_username: vsc,
#          vsc_static_route_list: { 0.0.0.0/1 } }
#
#    # ENVIRONMENT
#    # The hostname or IP address of the ansible machine
#    ansible_deployment_host: 135.227.181.232
#    # The VMs require interfaces, usually network bridges, on the target hypervisor system to connect
#    # to. These are the names of the network bridges that you have already configured for that purpose.
#    # These bridges are *not* created by Metro.
#    mgmt_bridge: "virbr0"
#    data_bridge: "virbr1"
#    # Destination directory for qcow2 images on the hypervisors.
#    images_path: "/var/lib/libvirt/images/"
#    # NTP servers the VSC, VSD, VNS-UTILITY and VSTAT should sync to.
#    # One or more ntp servers are required
#    # Please note: the NTP servers need to be specified in dotted decimal format (as below). 
#    ntp_server_list:
#      - 135.227.181.232
#      - 128.138.141.172
#    # DNS configuration
#    # One or more dns servers are required
#    dns_server_list:
#      - 192.168.122.1
#      - 128.251.10.145
#    # The dns search domain
#    dns_domain: example.com
#    # the timezone of the deployment location
#    timezone: US/Pacific
#    # yum params for the deployment.
#    yum_proxy: "NONE"
#    yum_update: yes
#    yum_pin: yes
#    # vsd architect/API auth params
#    vsd_auth:
#      username:  csproot
#      password:  csproot
#      enterprise: csp
#      api_url: 'https://192.168.122.201:8443'  
#    # vcenter params
#    vcenter:
#      username: administrator@vsphere.local
#      password: Alcateldc
#      datacenter: Datacenter
#      cluster: Management
#      datastore: datastore
#      ovftool: /usr/bin/ovftool
```
