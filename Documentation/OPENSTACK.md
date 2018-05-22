# Deploying Nuage Networks Components in OpenStack with MetroAG (limited support)
## Internal Lab Use Only. Not for Customer Use.
The following components/roles are supported by MetroAG in OpenStack.
### Deploy Infra VM
You can deploy an infra VM that acts as a private DNS server and NTP server for VSD and VSC.
`vsd-deploy` role and `vsc-deploy` role automatically populate their respective DNS entries with the hostname and IP addr mappings.
### Deploy VSD (Standalone or HA)
To deploy VSD in OpenStack you must upload VSD qcow2 image to glance. You must also create network and a flavor that is inline with the VSD resource requirements. (refer to VSP Install Guide).
### Deploy VSC (Single or pair without BGP support)
To deploy VSC in OpenStack you must upload VSC qcow2 image to glance. You must also create mgmt, control networks and a flavor that is inline with VSC resource requirements. (refer to VSP Install Guide).
### Deploy VSTAT (Standalone)
To deploy VSTAT (Elastic Search VM) you must upload VSTAT qcow2 image to glance. You must also create network and a flavor that is inline with VSTAT resource requirements (refer to VSP Install Guide).
### OSC (one)
You can deploy OpenStack Controller (OSC) using packstack with `osc-predeploy` and `osc-deploy` roles. You must upload a cloud image (CentOS/RHEL 7 only) with cloud-init support to glance. Supply the network, flavor and OpenStack release string as well. You may deploy the OpenStack plugin from a tar-gz archive. You may automatically unzip the archive with the nuage_unzip.yml playbook by defining `nuage_zipped_files_dir` and `nuage_unzipped_files_dir` in `build_vars.yml`, then running `./metro-ansible nuage_unzip.yml`.
### Deploy OSC Computes (One or more) and Add Them to OSC with VRS Packages
You can deploy compute VMs that will be managed by OSC with `os-compute-predeploy` and `os-compute-deploy` roles. `os-compute-postdeploy` role will replace the OVS packages in these compute VMs with Nuage VRS packages. The user requirements are the same as for OSC.
### VRS and OpenStack Compute Nodes Integration
Integrating VRS with OpenStack Compute nodes requires user to provide information (ip addresses) of compute nodes. VRS will be deployed onto these nodes, by replacing OVS packages. A sample yml file can be found in [examples](../examples/build_vars.yml.VRSOnly). Following are the steps to be followed in the same order for successful integration

1. Edit build_vars.yml according to [examples](../examples/build_vars.yml.VRSOnly)
2. Run ./metro-ansible nuage_unzip.yml -vvv
3. Run ./metro-ansible build.yml -vvv
4. Run ./metro-ansible vrs_predeploy.yml -vvv
5. Run ./metro-ansible vrs_deploy.yml -vvv
6. Finally run ./metro-ansible vrs_oscompute_integration.yml -vvv
## VSD-OSC Integration
`vsd-osc-integration` role helps to integrate OpenStackController(OSC) with VSD by making necessary changes to horizon, nova and neutron plugin files on OSC. This role can be run individually provided, OSC and VSD are installed by user. Prior to running this role/playbook, user needs to provide information related to e.g. openstack release, nuage openstack plugins dir, etc. A sample yml file can be found in [examples](../examples/build_vars.yml.vsd_osc_integration). A sample workflow for vsd-osc integration is defined below.

1. Edit build_vars.yml according to [examples](../examples/build_vars.yml.vsd_osc_integration)
2. Provide vsd login info in uesr_creds.yml
3. Run ./metro-ansible nuage_unzip.yml -vvv
4. Run ./metro-ansible build.yml -vvv
5. Finally run ./metro-ansible vsd_osc_integration.yml -vvv

### Snapshots and Backup
`os-snapshot` role is used to make backups of an entire project or set of VMs in a project. These snapshots are downloaded to local machine. Currently they are not archived or exported to a remote machine. So, make sure the local machine has enough storage.

For details about build and nuage-unzip roles and how to execute them please refer to [BUILD.md](BUILD.md) file.
### Running playbooks
Refer to [README.md](/README.md) for the organization of playbooks.
All the above roles/components can be run individually with `./metro-ansible <playbook>.yml` command.
# Reference

For reference, here is a description of the contents of the `build-vars.yml` file for OpenStack, with comments:

```
# Paths to find zipped (tar.gz) files and unzipped files (e.g. qcow2)
# Both are required to run the nuage_unzip role. nuage_unzipped_files_dir
# is required when one or more operation lists, below, are set to 'install'
# or 'upgrade'.
#    nuage_zipped_files_dir: "/home/caso/nfs-data/4.0.R7/nuage-packed"
#    nuage_unzipped_files_dir: "/home/caso/nfs-data/4.0.R7/nuage-unpacked"
#
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
#    # NTP Configuration (must be dotted-decimal format)
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
#
#    VSD params
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
```

## Questions, Feedback, and Contributing
Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
