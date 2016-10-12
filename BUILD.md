# build and reset-build

The build playbook (`build.yml`) is used to automatically populate a number of custom variable files for the operation of the metro playbooks. Running `./metro-playbook build.yml` will use the variables defined in `build.yml` to create a hosts file, populate a host_vars directory, populate a group_vars directory, and make a few additional variable changes as required. The `build.yml` playbook will do all the work for you.

Note that the syntax of the contents of `build.yml` must be precise. If things get messed up, we have provided the `reset_build.yml` playbook to let you start over. *When you run `./metro-ansible rest_build.yml`, the contents of `build.yml` will be overwritten, the hosts file will be destroywed, the host_vars directory will be destroyed, and the group_vars directory will be destroyed. The variable configuration of metro will be reset to factory settings! You may lose your work!* A backup copy of `build.yml` will be created as `build.bak` just in case you didn't mean it.

To run the build, execute:

`ansible-playbook build.yml`

or

`./metro-ansible build.yml`

To reset the build to factoery settings, execute:

`ansible-playbook reset_build.xml`

or

`./metro-ansible rest_build.yml`

# Reference

For reference, here is a description of the contents of the `build.yml` file, with comments:

```
#- hosts: localhost
#  gather_facts: no
#  roles:
#    - build
#  vars:
#    # When True or undefined, all VSDs will be configured stand-alone. When False
#    # we will expect 3 VSD definitions, below, for clustered deployment.
#    vsd_standalone: True
#    # The ansible server path where the VSD qcow2 image will be copied from
#    vsd_qcow2_path: "/home/caso/"
#    # The name of the VSD qcow2 file
#    vsd_qcow2_file_name: "VSD-4.0.3_32.qcow2"
#    # A dictionary of params for 0 or more VSDs
#    # Note: Multiple VSDs can be deployed from the same qcow2 file
#    myvsds:
#          # The fqdn of this VSD instance
#      - { hostname: vsd1.example.com,
#          # The hypervior target where this VSD instance will be run
#          target_server: 135.227.181.232,
#          # The IP address of this VSD instance
#          mgmt_ip: 192.168.122.201,
#          # The gateway IP address of this VSD instance
#          mgmt_gateway: 192.168.122.1,
#          # The netmask of this VSD instance
#          mgmt_netmask: 255.255.255.0 }
#    # The ansibe server path where the VSC qcow2 will be copied from
#    vsc_qcow2_path: "/home/caso/",
#    # The file name of this VSC qcow2
#    vsc_qcow2_file_name: "vsc_singledisk.qcow2" }
#    # A dictionary of params for 0 or more VSCs
#    # Note: Multiple VSCs can be deployed from the same qcow2 file
#    myvscs:
#      - { hostname: vsc1.example.com,
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
#    # The path on the ansible host from which VRS packages will be copied
#    vrs_package_path: "/home/caso/",
#    # A list of the packages to be installed on the VRS node
#    # Note that for RedHat OS family one VRS package is required.
#    # For example:
#    # vrs_package_file_name_list: { "nuage-openvswitch-3.2.9-323.el7.x86_64.rpm" }
#    # But for Debian OS family, three VRS packages are required.
#    # For example:
#    # vrs_package_file_name_list: " "nuage-openvswitch-common_3.2.9-323.amd64.deb", "nuage-openvswitch-switch_3.2.9-323.amd64.deb", "nuage-python-openvswitch_3.2.9-323_all.deb" } 
#    #
#    vrs_package_file_name_list: { "nuage-python-openvswitch_4.0.3-25_all.deb", "nuage-openvswitch-common_4.0.3-25_all.deb", "nuage-openvswitch-switch_4.0.3-25_amd64.deb"} }
#    # When True, install dockermon on the VRS. When False, don't.
#    dockermon_install: True
#    # The file name of the dockermon package
#    dockermon_package_file_name: "nuage-docker-monitor_4.0.3-25_all.deb" }
#    # A dictionary of params for 0 or more VRSs
#    # Note: Multiple VRS nodes can be configured from the same packages
#    myvrss:
#          # The node upon which VRS will be installed. Assume node is up and running...
#      - { node_ip_addr: 135.227.181.232,
#          # The active VSC IP address for this VRS node
#          active_controller_ip: 192.168.122.202,
#          # The standby VSC IP address for this VRS node
#          standby_controller_ip: 192.168.122.203 }
#    # The path on the ansible host from which VSTAT qcow2 images will be copied
#    vstat_qcow2_path: "/home/caso/",
#    # The file name of the qcow2 image
#    vstat_qcow2_file_name: "hd_template.qcow2" }
#    # A dictionary of params for 0 or more VSTAT instances
#    # Note: Multiple VSTAT instances can be copied from the same qcow2
#    myvstats:
#          # The hostname or IP address for this VSTAT instance
#      - { hostname: vstat1.example.com,
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
#    # When True VNS specific configuration is triggered in the VSD and VSC
#    vns: False
#    # The path on the ansible host from which PROXY qcow2 images will be copied
#    vnsutil_qcow2_path: "/home/caso/"
#    # The file name of the qcow2 image
#    vnsutil_qcow2_file_name: "vns-util-0.0_98.qcow2"
#    # A dictionary of params for 0 or more PROXY instances
#    # Note: Multiple PROXY instances can be copied from the same qcow2
#    myvnsutils:
#          # The hostname or IP address for this PROXY instance
#      - { hostname: proxy.example.com,
#          # The hypervior target where this PROXY instance will be run
#          target_server: 135.227.181.232,
#          # The management IP address of this PROXY instance
#          mgmt_ip: 10.0.0.50,
#          # The management gateway IP address of this PROXY instance
#          mgmt_gateway: 10.0.0.1,
#          # The management network netmask of this PROXY instance
#          mgmt_netmask: 255.255.255.0,
#          # The data network IP address for this PROXY instance
#          # This also the interface that run DHCP/DNSMASQ servers
#          # NSGV VM sends DHCP requests to this interface. Hence acts as uplink
#          data_ip: 10.0.1.50,
#          # The data network subnet address for this PROXY instance
#          # The subnet is configured in DHCP conf file 
#          data_subnet: 10.0.1.0,
#          # The data network netmask of this PROXY instance
#          data_netmask: 255.255.255.0,
#          # NSGV VM IP addr.
#          # This IP along with MAC addr is used to serve the DHCP client request coming from NSGV VM
#          nsgv_ip: 10.0.1.60,
#          # NSGV VM MAC address
#          nsgv_mac: '52:54:00:88:85:12',
#          # The FQDN for the VSD. Used to create certs for PROXY VM      
#          vsd_fqdn: vsd.example.com}
#    # The path on the ansible host from which PROXY qcow2 images will be copied
#    nsgv_qcow2_path: "/home/caso/"
#    # The file name of the qcow2 image
#    nsgv_qcow2_file_name: "ncpe_centos7.qcow2"
#    # A dictionary of params for only 1 NSGV instance for current release
#    mynsgvs:
#          # Define only hostname for this NSGV instance
#          # Do not add domain to the host name
#      - { hostname: nsgv,
#          # The hypervior target where this PROXY instance will be run
#          target_server: 135.227.181.232,
#          # NSGV VM mac addr that goes in to XML config file
#          nsgv_mac: '52:54:00:88:85:12'}
#    # The hostname or IP address of the ansible machine
#    ansible_host: 135.227.181.232
#    # The names of the network bridges that are required on the target hosts
#    mgmt_bridge: "virbr0"
#    data_bridge: "virbr1"
#    access_bridge: "access"
#    # Destination directory for qcow2 images on the hypervisors.
#    images_path: "/var/lib/libvirt/images/"
#    # The public ssh key of the ansible user on the deployment host
#    ansible_user_ssh_key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDha+H5IjOGGQ0VPo+WQm9uEDDkm6t5B56GQvivqUmK7QvWA8bYXSqmO4gp3zi6QZ558yHYWMrLS8ZGn93sDs68y24ROnaWJfj4dlp7mHsHVdP3yASeu9xW10p7WuEbriVoOjpX81+BsQwM6jiPzt+7VcbMrfL+Lo08aYW/XZxFe4ogk34AYo1t2eDmxROBk3aZ4hF4yvr0z/M92p4oDoU4FRFHYoAR5Kr8LQk9yGccGjmNFDSxhNZMkEHl0dmpb17xR7f9gbruBHe4NDFcfbCMHxC80uX1QKzj8mNC7dzTA/0CeaDa24pRYNabPHWmaijaQi6pFqPzIPKG48VfMzNn caso@cas-cs2-010"
#    # NTP servers the VSC, VSD, PROXY and VSTAT should sync to.
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
