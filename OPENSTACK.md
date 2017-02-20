# Support for deploying VSP components in OpenStack through metro(limited support)
# Note: This is purely for internal lab. Not meant for customer use.

## Overview

Using metro, users can deploy VSP components into OpenStack. These are the following components/roles supported by metro on OpenStack.

1. Deploy Infra VM
2. Deploy VSD (Standalone or HA)
3. Deploy VSTAT (Standalone)
4. Deploy VSC (1 or in pair without BGP support)
5. Deploy OSC (1)
6. Deploy OSC Computes (1 or more) and add them to OSC with VRS packages
7. VSD-OSC intergaration
8. Create Snapshot of project or VMs

## Details

### Infra VM

An infra VM is deployed to act as private DNS server and ntp server for VSD and VSC. The DNS entries are automatically populated with the hostname and IP addr mappings of VSD and VSC with the help of vsd-deploy and vsc-deploy roles. For this reason the user has to specify the infra VM FQDN in VSD and VSC build-vars (see reference below).

### VSD 

Deloying VSD in OpenStack requires the user to upload VSD qcow2 image to glance. For this release, the user is also required to create network and create a flavor that is inline with VSD resource requirements (refer VSP install guide). Standalone or HA deployments are supported

### VSC

Deploying VSC in OpenStack requires the user to upload VSC qcow2 image to glance. For this release, the user is also required to create a mgmt, control networks and create a flavor that is inline with VSC resource requirements (refer VSP install guide). Single or Pair(without BGP config) of VSC deployment is supported.

### VSTAT (Elastic Search VM) 

Deloying VSTAT in OpenStack requires the user to upload VSTAT qcow2 image to glance. For this release, the user is also required to create network and create a flavor that is inline with VSTAT resource requirements (refer VSP install guide). Only standalone mode is tested and supported.

### OSC

`osc-predploy` and `osc-deploy` roles are used to deploy OpenStack Controller (OSC) using packstack. The user needs to upload a cloud image (only CentOS/RHEL 7 are supported) with cloud-init support to glance. The netowrk, flavor and OpenStack release string needs to be supplied by user as well.
User needs to define a folder with name `nuage_os` and place nuage openstaclk plugin tar file in it. This folder needs to be defined under `nuage_packed_src_path` if `nuage_already_unpacked: False` or `nuage_packed_dst_path` if `nuage_already_unpacked: True` in `build.yml`

### OSC Computes

`os-compute-predeploy` and `os-compute-deploy` roles are used in deploying compute vms that will be managed by OSC. `os-compute-postdeploy` role will replace the ovs packages in thesecompute vms with Nuage VRS packages. The user requirements are same as OSC.

### VSD-OSC intergration

`vsd-osc-config` role helps to integrate OSC with VSD by making necessary changes to horizon and nuetron plugin files. It will also add csproot user to CMS group on VSD.

### Snapshots and backup

`os-snapshot` roles is used to make backups of an entire project or set of VMs in a project. These snapshots are downloaded to local machine. Currently they are not archived or exported to a remote machine. So, make sure the local machine has enough storage.

For details about build and nuage-unpack roles and how to execute them please refer to `BUILD.md` file.

## Runnning playbooks

For playbook organization please refer to `playbook organization` section of `README.md`
All the above roles/components can be run individually with `./metro-ansible <playbook>.yml` command

# Reference

For reference, here is a description of the contents of the `build-vars.yml` file for OpenStack, with comments:

```
#    # The directory where the Nuage Networks binariy archives are located. This is only
#    # required if nauge_already_unpacked == false. See below.
#    nuage_packed_src_path: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where to extract the relevant Nuage Networks binaries to
#    nuage_unpacked_dest_path: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Parameter to define whether binaries have already been extracted
#    # If true, the playbooks will *not* unpack. Files in nnuage_unpacked_dest_path
#    # will be used as is. If false, the nuage_unpack role will be executed.
#    nuage_already_unpacked: true
#    # Parameter used to define the Hypervisor-Architecture (One of: el6|el7|ubuntu)
#    nuage_target_architecture: "el7"
#    # Nuage OpenStack release
#    # required to populate/unpack nuage openstack packages
#    # supported OpenStack release for metro - liberty, mitaka
#    nuage_os_release: "liberty"
#    VSD
#    # When True or undefined, all VSDs will be configured stand-alone. 
#    # Only standlone mode is supported on OpenStack through metro
#    vsd_standalone: True
#    # A dictionary of params for INFRA server
#    myinfras:
#          # The fqdn of this INFRA instance
#      - { hostname: infra.example.com,
#          # The target server type where this INFRA instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True. 
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10 
#          # INFRA image to be used. Must exist on OpenStack
#          infra_image: centos7,
#          # INFRA flavor to be used. Must exist  on OpenStack
#          infra_flavor: m1.medium,
#          # INFRA network. Must exist on OpenStack
#          infra_network: mgmt 
#          # INFRA subnet. Required when dhcp is set to False
#          infra_subnet: mgmt_subnet }
#
#    VSD
#    # A dictionary of params for 1 VSD
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vsd1.example.com,
#          # The target server type where this VSD instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True. 
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10 
#          # VSD image to be used. Must exist on OpenStack
#          vsd_image: vsd-r4,
#          # VSD flavor to be used. Must exist  on OpenStack
#          vsd_flavor: m1.xlarge,
#          # VSD network. Must exist on OpenStack
#          vsd_network: mgmt,
#          # VSD subnet. Required when dhcp is set to False 
#          vsd_subnet: mgmt_subnet, 
#          # INFRA server vm fqdn name. This is optional. If not set, user has to take care of DNS entries.
#          infra_server_name: infra.example.com }
#
#    VSC
#    # A dictionary of params for 1 VSC
#    myvscs:
#          # The fqdn of this VSC instance
#      - { hostname: vsc1.example.com,
#          # The target server type where this VSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True.
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10,
#          # Required when dhcp is set to False
#          control_ip: 10.0.0.10,
#          # VSC image to be used. Must exist on OpenStack
#          vsc_image: vsc-r4,
#          # VSC flavor to be used. Must exist  on OpenStack
#          vsc_flavor: vsc-r4,
#          # VSC management network. Must exist on OpenStack
#          vsc_mgmt_network: mgmt,
#          # VSC management subnet. Required when dhcp is set to False  
#          vsc_mgmt_subnet: mgmt_subnet,
#          # VSC control network. Must exist on OpenStack
#          vsc_control_network: control_net, 
#          # VSC control subnet. Required when dhcp is set to False
#          vsc_control_subnet: control_subnet,
#          # The FQDN of the VSD this VSC should conect to
#          vsd_fqdn: vsd1.example.com,
#          # The system IP address and name for this VSC instance
#          system_ip: 1.1.1.2,
#          # The XMPP user name for login to VSD
#          xmpp_username: vsc,
#          # INFRA server vm fqdn name. This is optional. If not set, user has to take care of DNS entries.
#          infra_server_name: infra.example.com }
#
#    VSTAT
#    # A dictionary of params for 1 VSTAT
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vstat1.example.com,
#          # The target server type where this VSTAT instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True.
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10
#          # VSTAT image to be used. Must exist on OpenStack
#          vstat_image: vstat-r4,
#          # VSTAT flavor to be used. Must exist  on OpenStack
#          vstat_flavor: m1.xlarge,
#          # VSTAT network. Must exist on OpenStack
#          vstat_network: mgmt,
#          # VSTAT subnet. Required when dhcp is set to False  
#          vstat_subnet: mgmt_subnet,
#          # INFRA server vm fqdn name. This is optional. If not set, user has to take care of DNS entries.
#          infra_server_name: infra.example.com }
#
#    OSC
#    # A dictionary of params for 1 OSC
#    myoscs:
#          # The fqdn of this OSC instance
#      - { hostname: osc1.example.com,
#          # The target server type where this OSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True.
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10
#          # OSC image to be used. Must exist on OpenStack
#          osc_image: cenots7,
#          # OSC flavor to be used. Must exist  on OpenStack
#          osc_flavor: m1.medium,
#          # OSC network. Must exist on OpenStack
#          osc_network: mgmt,
#          # OSC subnet. Required when dhcp is set to False  
#          osc_subnet: osc_subnet,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # VSD IP. This is later used in a rest proxy config file to integrate OSC with VSD
#          # Required when dhcp is set to False
#          vsd_ip: 192.168.10.20,
#          # VSD server name in OpenStack. Required when DHCP is set to True
#          vsd_server_name: vsd1.example.com}
#
#    OS Computes
#    # A dictionary of params for 1 or more OpenStack compute vms
#    myoscomputes:
#          # The fqdn of this OS-COMPUTE instance
#      - { hostname: oscompute1.example.com,
#          # The target server type where this OS-COMPUTE instance will run. Possible values: heat
#          target_server_type: heat,
#          # When set to True, DHCP based deployments are supported. Default is True.
#          # When set to False, Static IP based deployments are supported.
#          dhcp: False,
#          # Required when dhcp is set to False
#          mgmt_ip: 10.0.0.10,
#          # Required when dhcp is set to False
#          data_ip: 10.0.0.10,
#          # OS-COMPUTE image to be used. Must exist on OpenStack
#          compute_image: cenots7,
#          # OS-COMPUTE flavor to be used. Must exist  on OpenStack
#          compute_flavor: m1.medium,
#          # os compute management network. Must exist on OpenStack
#          compute_mgmt_network: mgmt,
#          # Compute management suwbnet. Required when dhcp is set to False
#          compute_mgmt_subnet: mgmt_subnet,
#          # os compute data network. Must exist on OpenStack
#          compute_data_network: data,
#          # Compute data subnet. Required when dhcp is set to False
#          compute_data_subnet: data_subnet,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # OSC Serer name. FQDN of the OpenStack Controller
#          osc_server_name: osc1.example.com,
#          # Primary vsc controller IP. This is used to configure VRS on the computes
#          # Required when DHCP is set to False
#          vsc_primary_ip: 192.168.10.21,
#          # secondary vsc controller IP. This is used to configure VRS on the computes
#          # Optional.
#          vsc_secondary_ip: 192.168.10.21,
#          # Primary vsc controller hostname in OpenStack. This is used to configure VRS on the computes
#          # Required when DHCP is set to True
#          vsc_primary_server: vsc1.example.com,
#          # Secondary vsc controller hostname in OpenStack. This is used to configure VRS on the computes
#          # Optional
#          vsc_primary_server: vsc1.example.com,
#          # VRS package path to find VRS package file
#          vrs_package_path: /home/caso/metro/vrs/,
#          # VRS package file name:
#          vrs_package_file_name_list: ['nuage-openvswitch-4.0.7-129.el7.x86_64.rpm'] }
#    OpenStack credentials for authentication
#    os_auth:
#          # The username for OpenStack project
#          username: admin
#          # Password for OpenStack project
#          password: admin
#          # OpenStack project name
#          project_name: jen
#          # OpenStack keystone url
#          auth_url: 'http://10.0.0.4:5000/v2.0'
#
#    # ENVIRONMENT
#    # The hostname or IP address of the ansible machine
#    ansible_deployment_host: 135.227.181.232
#    # NTP servers the INFRA VM can sync to
#    # One or more ntp servers are required
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
```
