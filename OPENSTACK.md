# Support for deploying VSP components in OpenStack through metro(limited support)
# Note: This is purely for internal lab. Not meant for customer use.

## Overview

Using metro, users can deploy VSP components into OpenStack. These are the following components/roles supported by metro on OpenStack.

1. Deploy Infra VM
2. Deploy VSD (Standalone only)
3. Deploy VSC (1)
4. Deploy OSC (1)
5. Deploy OSC Computes (1 or more) and add them to OSC with VRS packages
6. VSD-OSC intergaration
7. Create Snapshot of project or VMs

## Details

### Infra VM

An infra VM is deployed to act as private DNS server and ntp server for VSD and VSC. The DNS entries are automatically populated with the hostname and IP addr mappings of VSD and VSC with the help of vsd-deploy and vsc-deploy roles. For this reason the user has to specify the infra VM FQDN in VSD and VSC build-vars (see reference below).

### VSD 

Deloying VSD in OpenStack requires the user to upload VSD qcow2 image to glance. For this release, the user is also required to create network and create a flavor that is inline with VSD resource requirements (refer VSP install guide). Only standalone mode is tested and supported.

### VSC

Deploying VSC in OpenStack requires the user to upload VSC qcow2 image to glance. For this release, the user is also required to create a mgmt, control networks and create a flavor that is inline with VSC resource requirements (refer VSP install guide). Only a single VSC is supported.

### OSC

`osc-predploy` and `osc-deploy` roles are used to deploy OpenStack Controller (OSC) using packstack. The user needs to upload a cloud image (only CentOS/RHEL 7 are supported) with cloud-init support to glance. The netowrk, flavor and OpenStack release string needs to be supplied by user as well.

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
#    # required if nauge_unpacked == false. See below.
#    nuage_release_src_path: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where to extract the relevant Nuage Networks binaries to
#    nuage_unpacked_dest_path: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Parameter used to define the Hypervisor-Architecture (One of: el6|el7|ubuntu)
#    nuage_target_architecture: "el7"
#    # Parameter to define whether binaries have already been extracted
#    # If true, the playbooks will *not* unpack. Files in nnuage_unpacked_dest_path
#    # will be used as is. If false, the nuage_unpack role will be executed.
#    nuage_unpacked: true
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
#          # INFRA image to be used. Must exist on OpenStack
#          infra_image: centos7,
#          # INFRA flavor to be used. Must exist  on OpenStack
#          infra_flavor: m1.medium,
#          # INFRA network. Must exist on OpenStack
#          infra_network: mgmt }
#    # A dictionary of params for 1 VSD
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vsd1.example.com,
#          # The target server type where this VSD instance will run. Possible values: heat
#          target_server_type: heat,
#          # VSD image to be used. Must exist on OpenStack
#          vsd_image: vsd-r4,
#          # VSD flavor to be used. Must exist  on OpenStack
#          vsd_flavor: m1.xlarge,
#          # VSD network. Must exist on OpenStack
#          vsd_network: mgmt,
#          # INFRA server vm fqdn name
#          infra_server_name: infra.example.com }
#
#    VSC
#    # A dictionary of params for 1 VSC
#    myvscs:
#          # The fqdn of this VSC instance
#      - { hostname: vsc1.example.com,
#          # The target server type where this VSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # VSC image to be used. Must exist on OpenStack
#          vsc_image: vsc-r4,
#          # VSC flavor to be used. Must exist  on OpenStack
#          vsc_flavor: vsc-r4,
#          # VSC network. Must exist on OpenStack
#          vsc_management_network: mgmt,
#          # VSC control network. Must exist on OpenStack
#          vsc_control_network: control_net, 
#          # The FQDN of the VSD this VSC should conect to
#          vsd_fqdn: vsd1.example.com,
#          # The system IP address and name for this VSC instance
#          system_ip: 1.1.1.2,
#          # The XMPP user name for login to VSD
#          xmpp_username: vsc,
#          # INFRA server vm fqdn name
#          infra_server_name: infra.example.com }
#
#    # A dictionary of params for 1 OSC
#    myoscs:
#          # The fqdn of this OSC instance
#      - { hostname: osc1.example.com,
#          # The target server type where this OSC instance will run. Possible values: heat
#          target_server_type: heat,
#          # OSC image to be used. Must exist on OpenStack
#          osc_image: cenots7,
#          # OSC flavor to be used. Must exist  on OpenStack
#          osc_flavor: m1.medium,
#          # OSC network. Must exist on OpenStack
#          osc_network: mgmt,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # VSD IP. This is later used in a rest proxy config file to integrate OSC with VSD
#          vsd_ip: 192.168.10.20,
#          # Primary controller IP. This is used to configure VRS on the computes
#          primary_controller: 192.168.10.21 }
#
#    # A dictionary of params for 1 or more OpenStack compute vms
#    myoscomputes:
#          # The fqdn of this OS-COMPUTE instance
#      - { hostname: oscompute1.example.com,
#          # The target server type where this OS-COMPUTE instance will run. Possible values: heat
#          target_server_type: heat,
#          # OS-COMPUTE image to be used. Must exist on OpenStack
#          compute_image: cenots7,
#          # OS-COMPUTE flavor to be used. Must exist  on OpenStack
#          compute_flavor: m1.medium,
#          # OS-COMPUTE network. Must exist on OpenStack
#          compute_network: mgmt,
#          # OpenStack release num
#          # This is used for RedHat images to download OpenStack release related packages
#          # Possible and supported values 8 (Liberty) and 9 (Mitaka) 
#          os_release_num: 8, 
#          # OSC Serer name. FQDN of the OpenStack Controller
#          osc_server_name: osc1.example.com }
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
