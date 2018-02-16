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

`osc-predploy` and `osc-deploy` roles are used to deploy OpenStack Controller (OSC) using packstack. The user needs to upload a cloud image (only CentOS/RHEL 7 are supported) with cloud-init support to glance. The network, flavor and OpenStack release string needs to be supplied by user as well.
The user may be depoying the OpenStack plugin from a tar-gz archive. The archive may be automatically unzipped using the `nuage_unzip.yml` playbook. Define the `nuage_zipped_files_dir` and `nuage_unzipped_files_dir` in `build_vars.yml` and run `./metro-ansible nuage_unzip.yml`. 

### OSC Computes

`os-compute-predeploy` and `os-compute-deploy` roles are used in deploying compute vms that will be managed by OSC. `os-compute-postdeploy` role will replace the ovs packages in thesecompute vms with Nuage VRS packages. The user requirements are same as OSC.

### VRS and OpenStack Compute nodes integration

Integrating VRS with OpenStack Compute nodes requires user to provide information (ip addresses) of compute nodes. VRS will be deployed onto these nodes, by replacing OVS packages. A sample yml file can be found in [examples](../examples/build_vars.yml.VRSOnly). Following are the steps to be followed in the same order for successful integration

1. Edit build_vars.yml according to [examples](../examples/build_vars.yml.VRSOnly)
2. Run ./metro-ansible nuage_unzip.yml -vvv
3. Run ./metro-ansible build.yml -vvv
4. Run ./metro-ansible vrs_predeploy.yml -vvv
5. Run ./metro-ansible vrs_deploy.yml -vvv
6. Finally run ./metro-ansible vrs_oscompute_integration.yml -vvv

### VSD-OSC intergration

`vsd-osc-integration` role helps to integrate OpenStackController(OSC) with VSD by making necessary changes to horizon, nova and neutron plugin files on OSC. This role can be run individually provided, OSC and VSD are installed by user. Prior to running this role/playbook, user needs to provide information related to e.g. openstack release, nuage openstack plugins dir, etc. A sample yml file can be found in [examples](../examples/build_vars.yml.vsd_osc_integration). A sample workflow for vsd-osc integration is defined below.

1. Edit build_vars.yml according to [examples](../examples/build_vars.yml.vsd_osc_integration)
2. Provide vsd login info in uesr_creds.yml
3. Run ./metro-ansible nuage_unzip.yml -vvv
4. Run ./metro-ansible build.yml -vvv
5. Finally run ./metro-ansible vsd_osc_integration.yml -vvv

### Snapshots and backup

`os-snapshot` roles is used to make backups of an entire project or set of VMs in a project. These snapshots are downloaded to local machine. Currently they are not archived or exported to a remote machine. So, make sure the local machine has enough storage.

For details about build and nuage-unzip roles and how to execute them please refer to `BUILD.md` file.

## Runnning playbooks

For playbook organization please refer to `playbook organization` section of `README.md`
All the above roles/components can be run individually with `./metro-ansible <playbook>.yml` command

# Reference

For reference, here is a description of the contents of the `build-vars.yml` file for OpenStack, with comments:

```
#    # The directory where the Nuage Networks zipped archives are located. This is only
#    # required if you will be running the nuage_unzip.yml playbook.
#    nuage_zipped_files_dir: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where to extract/find the relevant Nuage Networks unzipped files
#    nuage_unzipped_files_dir: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Nuage OpenStack release
#    # required to populate/unzip nuage openstack packages
#    # supported OpenStack release for metro - liberty, mitaka
#    nuage_os_release: "liberty"
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
#    VSD params
#    vsd_sa_or_ha = ha for cluster, sa for standalone deployment
#    vsd_sa_or_ha: sa
#    VSD FQDN
#    Use xmpp fqdn for clustered VSDs and the vsd fqdn for stand alone
#    This variable must be populated for all the components except VRS deployment
#    vsd_fqdn_global: vsd1.example.com
#    vsd_operations_list = A list of the operations you intend for the VSD. The
#    list could include 1 or more of the following:
#    - install
#    - upgrade
#    - health
#    - TBD
#    # vsd_operations_list:
#       - install
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
#    VSC params
#    vsc_operations_list = A list of the operations you intend for the VSC. The
#    list could include 1 or more of the following:
#    - install
#    - upgrade
#    - health
#    - TBD
#    # vsc_operations_list:
#       - install
#    myvscs is a collection of parameters for VSCs.
#    One set of parameters is required for each VSC.
#    Do not update {{ vsd_fqdn_global }} here as it reads from previous section
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
#          vsd_fqdn: "{{ vsd_fqdn_global }}",
#          # The system IP address and name for this VSC instance
#          system_ip: 1.1.1.2,
#          # The XMPP user name for login to VSD
#          xmpp_username: vsc,
#          # INFRA server vm fqdn name. This is optional. If not set, user has to take care of DNS entries.
#          infra_server_name: infra.example.com }
#
#    Stats VM (ElasticSearch) params
#    vstat_operations_list = A list of the operations you intend for the ES node. The
#    list could include 1 or more of the following:
#    - install
#    - upgrade
#    - health
#    - dns (specified when deploying the VSTAT image as a DNS server)
#    - TBD
#    # vstat_operations_list:
#       - install
#    myvstats is a collection of parameters for the VSTAT.
#    One set of parameters is required for each VSTAT.
#    Do not update {{ vsd_fqdn_global }} here as it reads from previous section
#    myvstats:
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
#          vsd_fqdn: "{{ vsd_fqdn_global }}" 
#          # INFRA server vm fqdn name. This is optional. If not set, user has to take care of DNS entries.
#          infra_server_name: infra.example.com }
#
#    OpenStack Controller params
#    osc_operations_list = A list of the operations you intend for the ES node. The
#    list could include only one option from the following:
#    - install or
#    - integrate_with_vsd
#    # osc_operations_list:
#      - install
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
#          # Possible and supported values 10 (Newton) and 11 (Ocata) 
#          os_release_num: 11, 
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
#          # Possible and supported values 10 (Newton) and 11 (Ocata) 
#          os_release_num: 11, 
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
