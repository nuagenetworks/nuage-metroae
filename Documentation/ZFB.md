# zfb_vars.yml 

The zfb_vars.yml file is used to generate Zero Factor Bootstrapping profile for NSGV VMs on the VSD architect. This file is directly consumed by a python script that talks to VSD APIs to generate ISO file needed for ZFB of NSGVs. 

# Reference

Here is a description of the contents of the `zfb_vars.yml` file, with comments:

```
#    # License to operate VSD architect
#    vsd_license_file: "/path/to/license/file"
#    # A sample origanization. NSGV will be part of this Org
#    organization:
#      # Name of the organization
#      name: metro-test
#      # Name of NSGV. This will be used to represent it in VSD architect
#      nsg_name: NSG_US
#    # CSP credentials are used to access the VSD API and create profile
#    # csproot is only one example of supported users. Other supported users include
#    # the CMS user and those with administrative privileges across all enterprises.
#    csp:
#      # CSP username
#      username:  csproot
#      # CSP password
#      password:  csproot
#      # CSP org name
#      enterprise: csp
#      # VSD IP address/hostname
#      api_url: 'https://192.168.122.211:8443'
#    # The proxy user is required and will be added to the CSP root user group
#    user_data:
#      # First name of the proxy user
#      firstName: metro
#      # Last name of the proxy user
#      lastName: metro
#      # Email address of the proxy user
#      email: test@example.com
#      # Only Encrypted password
#      password: a94a8fe5ccb19ba61c4c0873d391e987982fbbd3
#    # NSG infrastructure template that contains Utility VM DNS name
#    vns_nsg:
#      # Name for the template
#      name: metro_vns
#      # NSG template name. This will be poped out of the dictionary to use elsewhere
#      nsg_template_name: metro-test
#      # DNS name of VNS Utility VM
#      proxyDNSName: jenkinsvnsutil1.example.com
#    # VSC template
#    vns_vsc:
#      # Name for the vsc template
#      name: metro_vsc
#      # IP address of the primary VSC controller
#      firstController: 192.168.100.202
#      # IP address of the secondary controller. This is optional
#      secondController: 192.168.100.203
#    # NSG ports definition
#    nsg_ports:
#      # This port is used as an Uplink 
#      network_port:
#        # Name for the port to identify in VSD
#        name: port1_network
#        # Name for the port to identify in NSGV
#        physicalName: port1
#        # Since it is as Uplink, type is NETWORK
#        portType: NETWORK
#      # Access port definiton
#      access_port:
#        # Name for the port to identify in VSD
#        name: port2_access
#        # Name for the port to identigy in NSGV
#        physicalName: port2
#        # User defined VLAN range
#        VLANRange: '0-100'
#        # VLAN id desired for access port
#        vlan_value: 20
```
