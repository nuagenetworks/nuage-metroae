# zfb.yml 

The zfb.yml file is used to generate Zero Factor Bootstrapping profile for NSGV VMs on the VSD architect. This file is directly consumed by a python script that talks to VSD APIs to generate ISO file needed for ZFB of NSGVs. 

# Reference

Here is a description of the contents of the `zfb.yml` file, with comments:

```
# vsd_license: "vsd license string goes here"
# License to operate VSD architect
# organization:
# A sample origanization. NSGV will be part of this Org
#   name: metro-test
#   Name of the organization
#   nsg_name: NSG_US
#   Name of NSGV. This will be used to represent it in VSD architect
# csp:
# CSP credentials are used to access the VSD API and create profile
#   username:  csproot
#   CSP username
#   password:  csproot
#   CSP password
#   enterprise: csp
#   CSP org name
#   api_url: 'https://192.168.122.211:8443'
#   VSD IP address/hostname
# user_data:
#  A proxy used is needed and should be added to CSP root user group 
#   firstName: metro
#   First name of the proxy user
#   lastName: metro
#   Last name of the proxy user
#   userName: proxy
#   User name should be proxy
#   email: test@caso.com
#   Email address of the proxy user
#   password: a94a8fe5ccb19ba61c4c0873d391e987982fbbd3
#   Only Encrypted password
# vns_nsg:
# NSG infrastructure template that contains Utility VM DNS name
#   name: metro_vns
#   Name for the template
#   nsg_template_name: metro-test
#   NSG template name. This will be poped out of the dictionary to use elsewhere
#   proxyDNSName: jenkinsvnsutil1.example.com
#   DNS name of VNS Utility VM
#   useTwoFactor: False
#   Should be false for ZFB method
#   upgradeAction: NONE
#   Chose to whether to upgrade
# vns_vsc:
# VSC template
#   name: metro_vsc
#   Name for the vsc template
#   firstController: 192.168.100.202
#   IP address of the primary VSC controller
#   secondController: 192.168.100.203
#   IP address of the secondary controller. This is optional
# nsg_ports:
# NSG ports definition
#   network_port:
#   This port is used as an Uplink 
#     name: port1_network
#     Name for the port to identify in VSD
#     physicalName: port1
#     Name for the port to identify in NSGV
#     portType: NETWORK
#     Since it is as Uplink, type is NETWORK
#   access_port:
#   Access port definiton
#     name: port2_access
#     Name for the port to identify in VSD
#     physicalName: port2
#     Name for the port to identigy in NSGV
#     portType: ACCESS
#     Since it is as Access port, type is ACCESS
#     VLANRange: '0-100'
#     User defined VLAN range
#     vlan_value: 20
#     VLAN id desired for access port
# iso_params:
# Parameters to generate ISO file for NSGV
#   mediaType: ISO
#   Remains ISO for KVM based deployments of NSGV
#   associatedEntityType: nsgatewaytemplate
#   This is constant. Should not be changed
#   NSGType: ANY
#   Change for desired NSG deployment
#   associatedEntityID: update
#   This is constant. Should not change

```
