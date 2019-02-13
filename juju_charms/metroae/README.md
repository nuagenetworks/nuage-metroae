# Overview

Nuage VSC
------------------

The principle use of this charm is with the Nuage VRS and Nuage VSD components. The VSC Charm orchestrates the deployment of the controller component of the VSP solution (VSC) within an OpenStack deployment .

This charm should be used with other principle charms to configure and control the data-path service units configured using the Nuage VRS Charms

NOTE: this charm relies on binaries that are distributed to customers of Nuage Networks VSP solution.

# Usage
=======
The VSC service is deployed as a KVM virtual machine. 
The VSC repository: The VSC VM (.qcow) image and its VM definition file are provided either as a payload or as an URL to customers to download and deploy on Juju machines.

This VSC VM image must be placed either in the 'payload' folder within the charm or as part of a valid repository URL prior 
to deployment.  The charm expects to find the image; if they are missing the install hook will error out.

The charm will use the VSC image and VM definition xml specified and deploy it on a kvm.

To Deploy:

    juju deploy nuage-vsc
	juju add-relation nuage-vsc nuage-vsd
	
# VSC VM (KVM) Configuration
The VSC service VM is required to have a minimum of 4GB of memory and a minimum of 4 cores. 

The VSC VM management IP address is a static IP address and is a configuration parameter of the VSC charm. 
In a MaaS deployment this IP address must be obtained from the IP range defined for the MaaS DHCP configuration.

The following nuage-vsc charm configuration parameters are required:
  vsc-vm-ip-address: "IP Address of the VSC VM"
  vsc-vm-default-gw: "Gateway that your VSC-VM will use to talk to other services in juju env like nauge-vsd
  vsc-vm-dns-server: "DNS Server which will be used to reslove the DNS for VSD-VM IP."
  vsc-vm-subnet-mask-length: "Length of the subnet mask for the VM IP"
  vsc-repository-url: "URL to get the Nuage VSC image. Basically this tar file contains three files: vsc.xml,vsc.qcow2 and bof.cfg"
 

## Known Limitations and Issues
MaaS 1.7 API does not yet support the API to obtain an IP address from the IP range defined for the MaaS DHCP configuration.

## Restrictions
This charm only support deployment with OpenStack Icehouse or better.

# Contact Information
Nuage Networks
755 Ravendale Drive                                  
Mountain View CA 94043
info@nuagenetworks.net


