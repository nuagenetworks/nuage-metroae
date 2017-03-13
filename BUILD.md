# build and reset-build playbooks

The build playbook (`build.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-ansible build.yml` will use the variables defined in `build_vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build.yml` playbook will do all the work for you.

Note that the syntax of the contents of `build_vars.yml` must be precise. If things get messed up, we have provided the `reset_build.yml` playbook to let you start over. *When you run `./metro-ansible rest_build.yml`, the contents of `build_vars.yml` will be overwritten, the `hosts` file will be destroyed, the `host_vars` directory will be destroyed, and the `group_vars` directory will be destroyed. The variable configuration of metro will be reset to factory settings! You may lose your work!* A backup copy of `build_vars.yml` will be created with a proper timestamp in case you did not mean it.

To run the build, execute:

`ansible-playbook build.yml`

or

`./metro-ansible build.yml`

To reset the build to factory settings, execute:

`ansible-playbook reset_build.yml`

or

`./metro-ansible rest_build.yml`

# nuage_unpack playbook

When the `build.yml` playbook is executed, it expects to find Nuage software binaries (QCOW2, OVA, and Linux Package files) in specific places. You can either copy the proper files to their locations, shown below, or you can use the nuage_unpack.yml playbook to do the work for you. Simply specify the proper source and target directories in `build_vars.yml` and `nuage_unpack.yml` will do the heavy lifting.

Here are the expected paths to binaries.

```
<your_path>/vsd/qcow2/ (or <your_path>/vsd/ova/ for VMware)
<your_path>/vsc/
<your_path>/vrs/
<your_path>/dockermon/
<your_path>/vstat/
<your_path>/vns/nsg/
<your_path>/vns/nsg/aws/
<your_path>/vns/util/
```

# Reference

For reference, here is a description of the contents of the `build_vars.yml` file, with comments:

```
#    # The directory where the Nuage Networks binariy archives are located. This is only
#    # required for the `nuage_unpack.yml` playbook.
#    nuage_tar_gz_files_dir: "{{ ansible_env.HOME}}/nuage-release"
#    # The directory where the required Nuage Networks binaries (*.qcow2, *.ova, *.rpm, *.deb) exist
#    nuage_binary_files_dir: "{{ ansible_env.HOME}}/nuage-unpacked"
#    # Parameter used to define the Hypervisor-Architecture (One of: el6|el7|ubuntu)
#    nuage_target_architecture: "el7"
#    # Parameter to define the remote sudo username to use on target servers, e.g. hypevisors.
#    target_server_username: "root"
#    # Parameter to define the sudo username to use on the ansible server.
#    ansible_sudo_username: "root"
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
#    VRS
#    # When True, install dockermon on the VRS. When False, don't.
#    dockermon_install: True
#    # A dictionary of params for 0 or more VRSs
#    # Note: Multiple VRS nodes can be configured from the same packages
#    myvrss:
#          # VRS set one
#          # Friendly name for a set of vrs nodes
#      - { vrs_set_name: vrs_set_uswest2,
#          # OS type of the vrs nodes in this set, allowed values are el6/el7,u14.04/u16.04
#          vrs_os_type: u14.04,
#          # The active VSC IP address for this set of VRS nodes
#          active_controller_ip: 192.168.122.202,
#          # The standby VSC IP address for this set of VRS nodes
#          standby_controller_ip: 192.168.122.203,
#          # A list of node IP addresses upon which VRS will be installed. Assume nodes are up and running...
#          vrs_ip_list: [ 
#           192.168.122.101,
#           192.168.122.142 ] }
#          # VRS set two
#      - { vrs_set_name: vrs_set_uswest2,
#          vrs_os_type: el7,
#          active_controller_ip: 192.168.122.202,
#          standby_controller_ip: 192.168.122.203,
#          vrs_ip_list: [
#           192.168.122.83,
#           192.168.122.238 ] }
#          # VRS set three
#      - { vrs_set_name: vrs_set_uswest3,
#          vrs_os_type: u16.04,
#          active_controller_ip: 192.168.122.202,
#          standby_controller_ip: 192.168.122.203,
#          vrs_ip_list: [
#           192.168.122.236 ] }
#
#    VSTAT - ElasticSearch
#    # A dictionary of params for 0 or more VSTAT instances
#    # Note: Multiple VSTAT instances can be copied from the same qcow2
#    myvstats:
#          # The hostname or IP address for this VSTAT instance
#      - { hostname: vstat1.example.com,
#          # The target server type where this VSTAT instance will run. Possible values: kvm
#          target_server_type: kvm,
#          # The hypervior target where this VSTAT instance will be run
#          target_server: 135.227.181.232,
#          # The management IP address of this VSTAT instance
#          mgmt_ip: 192.168.122.204,
#          # The management gateway IP address of this VSTAT instance
#          mgmt_gateway: 192.168.122.1,
#          # The management network netmask of this VSTAT instance
#          mgmt_netmask: 255.255.255.0,
#          # The FQDN for the VSD this VSTAT instance will connect to
#          vsd_fqdn: vsd1.example.com }
#
#    VNSUTIL
#    # A dictionary of params for 0 or more VNS-UTILITY instances
#    # Note: Multiple VNS-UTILITY instances can be copied from the same qcow2
#    myvnsutils:
#          # The hostname or IP address for this VNS-UTILITY instance
#      - { hostname: proxy.example.com,
#          # The target server type where this VNS-UTILITY instance will run. Possible values: kvm
#          target_server_type: kvm,
#          # The hypervior target where this VNS-UTILITY instance will be run
#          target_server: 135.227.181.232,
#          # The management IP address of this VNS-UTILITY instance
#          mgmt_ip: 10.0.0.50,
#          # The management gateway IP address of this VNS-UTILITY instance
#          mgmt_gateway: 10.0.0.1,
#          # The management network netmask of this VNS-UTILITY instance
#          mgmt_netmask: 255.255.255.0,
#          # The data network IP address for this VNS-UTILITY instance
#          # This also the interface that run DHCP/DNSMASQ servers
#          # NSGV VM sends DHCP requests to this interface. Hence acts as uplink
#          data_ip: 10.0.1.50,
#          # The data network subnet address for this VNS-UTILITY instance
#          # The subnet is configured in DHCP conf file 
#          data_subnet: 10.0.1.0,
#          # The data network netmask of this VNS-UTILITY instance
#          data_netmask: 255.255.255.0,
#          # NSGV VM IP addr.
#          # This IP along with MAC addr is used to serve the DHCP client request coming from NSGV VM
#          nsgv_ip: 10.0.1.60,
#          # NSGV VM MAC address
#          nsgv_mac: '52:54:00:88:85:12',
#          # NSGV FQDN
#          # VNSUTIL vm can have multiple fqdn's. This var is used to set the fqdn that nsgv's use
#          # Default is set to inventory_hostname if not specified
#          nsgv_fqdn: data.example.com,
#          # The FQDN for the VSD. Used to create certs for VNS-UTILITY VM      
#          vsd_fqdn: vsd.example.com}
#
#    NSGV
#    # A dictionary of params for only 1 NSGV instance for current release
#    mynsgvs:
#          # Define only hostname for this NSGV instance
#          # Do not add domain to the host name
#      - { hostname: nsgv,
#          # The target server type where this NSGV instance will run. Possible values: kvm
#          target_server_type: kvm,
#          # The hypervior target where this NSGV instance will be run
#          target_server: 135.227.181.232,
#          # NSGV VM mac addr that goes in to XML config file
#          nsgv_mac: '52:54:00:88:85:12'}
#
#    # ENVIRONMENT
#    # The hostname or IP address of the ansible machine
#    ansible_deployment_host: 135.227.181.232
#    # The VMs require interfaces, usually network bridges, on the target hypervisor system to connect
#    # to. These are the names of the network bridges that you have already configured for that purpose.
#    # These bridges are *not* created by Metro.
#    mgmt_bridge: "virbr0"
#    data_bridge: "virbr1"
#    access_bridge: "access"
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
#    # vcenter params
#    vcenter:
#      username: administrator@vsphere.local
#      password: Alcateldc
#      datacenter: Datacenter
#      cluster: Management
#      datastore: datastore
#      ovftool: /usr/bin/ovftool
```
