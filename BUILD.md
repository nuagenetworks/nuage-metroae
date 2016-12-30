# build and reset-build playbooks

The build playbook (`build.yml`) is used to automatically populate a number of Ansible variable files for the operation of the metro playbooks. Running `./metro-playbook build.yml` will use the variables defined in `build-vars.yml` to create a `hosts` file, populate a `host_vars` directory, populate a `group_vars` directory, and make a few additional variable changes as required. The `build.yml` playbook will do all the work for you.

Note that the syntax of the contents of `build-vars.yml` must be precise. If things get messed up, we have provided the `reset_build.yml` playbook to let you start over. *When you run `./metro-ansible rest_build.yml`, the contents of `build-vars.yml` will be overwritten, the `hosts` file will be destroyed, the `host_vars` directory will be destroyed, and the `group_vars` directory will be destroyed. The variable configuration of metro will be reset to factory settings! You may lose your work!* A backup copy of `build-vars.yml` will be created with a proper timestamp in case you did not mean it.

To run the build, execute:

`ansible-playbook build.yml`

or

`./metro-ansible build.yml`

To reset the build to factory settings, execute:

`ansible-playbook reset_build.xml`

or

`./metro-ansible rest_build.yml`

# nuage_unpack playbook

When the `build.yml` playbook is executed, it will first check the setting for the parameter `nuage_unpacked` in the vars section of the plabook. When `nuage_unpacked` is set to `false`, the `nuage-unpack` role will be executed prior to setting other parameters. The `nuage_unpack` role is useful when you download the Nuage Networks software as a set of archives for each component of the solution. To deploy the software using Metro, only a few of the binaries in those archives are required. As such the `nuage-unpack` role will analyze all the archives, extract the necessary binaries, and store them in a configurable directory.

You can also choose to unpack the binaries yourself, skipping the `nuage-unpack` role by setting `nuage_unpacked` to `true` in `build.yml`. In such a case, the playbooks will assume that you have already unpacked the binaries into the appropriate locations, as shown below.

```
<your_path>/vsd
<your_path>/vsc
<your_path>/vrs
<your_path>/dockermon
<your_path>/vstat
<your_path>/vns/nsg
<your_path>/vns/nsg/aws
<your_path>/vns/util
```

You can also choose to run the `nuage-unpack` role manually by executing `./metro-ansible nuage_unpack.yml`
The `nuage-unpack` role also uses Ansible tags to limit the extraction or variable setting to a particular component of choice.
# Reference

For reference, here is a description of the contents of the `build-vars.yml` file, with comments:

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
#          # The node upon which VRS will be installed. Assume node is up and running...
#      - { node_ip_addr: 135.227.181.232,
#          # The active VSC IP address for this VRS node
#          active_controller_ip: 192.168.122.202,
#          # The standby VSC IP address for this VRS node
#          standby_controller_ip: 192.168.122.203 }
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
#    ansible_host: 135.227.181.232
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
