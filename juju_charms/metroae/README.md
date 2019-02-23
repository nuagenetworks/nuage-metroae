# Nuage Networks Metro Automation Engine (MetroÆ) Charm Beta

## Overview

The Nuage MetroÆ charm in its beta form is designed to deploy one Nuage VSC VM on a KVM server. In principle, this server can be any general-purpose Linux server running KVM in a MaaS environment. The target environment for this beta, however, is the VSC to be deployed on a Canonical OpenStack server running Ubuntu 18.04.

This charm should be used with other charms to configure and control the data-path service units configured using other Nuage Networks charms

NOTE: this charm relies on binaries that are distributed to customers of Nuage Networks VSP solution.

## Prerequisites

- VSC qcow2 image available via http URL (repository) in your environment
- Private key file for ssh to the target server (KVM hypervisor) available via http URL (repository)
- Properly configured MaaS server with a tagged bare-metal instance specifically for this VSC
- Bare-metal instance must be configured with a minimum of 4 GB of memory and 4 CPU cores.
- Bare-metal instance must be configured to be given a known, static IPv4 address
- Bare-metal instance must be configured to use a DNS server that can resolve the VSD FQDN

## Limitations

This beta version of the charm has the following limitations

- TLS is not enabled on the XMPP channel between the VSC and the VSD
- TLS is not enabled on the OpenFlow channel between the VSC and the VRS
- The IP address of the hypervisor on the bare-metal MaaS instance must be provided as input
- DNS for the MaaS instance must be configured to resolve the VSD FQDN that is provided as input  

## Usage

This charm is deployed via bundle file. The VSC service is a subordinate charm that must be bundled with a non-subordinate OS charm, e.g. ubuntu. It is suggested that the bundle file have the following general format:

```
machines:
  "1":
    series: bionic
    constraints: "tags=metro"
series: bionic
services:
  ubuntu:
    charm: cs:bionic/ubuntu
    num_units: 1
    to:
      - 1
  metroae:
    charm: ./metroae
    num_units: 0
    options:
      <insert options here...>
```

Notice that the machine declaration includes a tag. This tag must be set to the bare-metal MaaS intance that this VSC will be deployed to.

To Deploy:

`juju deploy <bundle_file.yaml>`

There are one or more sample bundle files in the charm's `bundles` directory.

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
