# Using a VMware vCenter environment to deploy Nuage using MetroAG

## Table of Content

- [Supported versions](#supported-versions)
  - [Nuage supported versions and components](#nuage-supported-versions-and-components)
  - [vSphere supported versions](#vsphere-supported-versions)
- [Prerequisites / Requirements](#prerequisites---requirements)
  - [Required packages](#required-packages)
  - [vCenter user requirements](#vcenter-user-requirements)
- [Configuration](#configuration)
  - [Specifying the vCenter host to use](#specifying-the-vcenter-host-to-use)
  - [Overwriting settings for specific components](#overwriting-settings-for-specific-components)
- [Deploying vCenter Integration Nodes](#deploying-vcenter-integration-nodes)
  - [VCIN deployment](#vcin-deployment)
  - [VCIN Active/Standby deployment](#vcin-active-standby-deployment)

## Supported versions

### Nuage supported versions and components

All versions starting from 4.0R11 and 5.0.1 are supported.

  **Note**: Support for VCIN Active/Standby deployment is only available for Nuage versions 5.2.2 and above.

The following Nuage components can be deployed on a vSphere environment using MetroAG:

* VSD
* VCIN (Active/Standby)
* ElasticSearch
* VSC
* VNS Utils
* NSG-V
* STC-V

### vSphere supported versions

The deployment of the Nuage components on a vSphere environment using MetroAG is supported on the same vSphere version as described in the Nuage Release Notes.

## Prerequisites / Requirements

### Required packages

The following software and python packages are required to be installed on the MetroAG Host.

 Package  | Command
 -------- | -------
 ovftool  | Download from the [VMware website](https://www.vmware.com/support/developer/ovf/)
 pyvmomi  | `pip install pyvmomi`
 jmespath | `pip install jmespath`

### vCenter user requirements

The vCenter user or users used to deploy or upgrade the Nuage components on a vSphere environment will require a minimum of the following permissions:

* Most of the VM actions for VMs in the resource pool the VMs need to be deployed in. This includes:
  * Creating and Deleting VMs
  * Changing the Power state of the VM
  * Executing commands through VMware tools
  * Deploy OVAs and OVFs
* (Optional) Create and update Distributed vSwitches and Distributed vSwitch Port Groups

## Configuration

To provide the general configuration for the deployment of the Nuage components on a vSphere environment, a set of configuration values has to be provided in the `build_vars.yml` file (or your own variables file).

The below example shows and explains the general configuration values needed for a vSphere deployment.

```yaml
vcenter:
  username: administrator@vsphere.local
  password: vmware
  datacenter: Datacenter
  cluster: Management
  datastore: Datastore
  resource_pool: Resourece Pool
  ovftool: /usr/bin/ovftool
```

* **vcenter.username**
  This is the username that will be used to connect to the vSphere environment, typically this will be in a username@domain.tld format when connecting to vCenter.
* **vcenter.password**
  This is the password that will be used to connect to the vSphere environment, for the user mentioned in `vcenter.username`.
* **vcenter.datacenter**
  This is the datacenter in vCenter in which the Nuage components will be deployed in by MetroAG. This name needs to exactly match with the name in vCenter for the Datacenter.
* **vcenter.cluster**
  This is the cluster in vCenter, part of the datacenter configured in `vcenter.datacenter`. The Nuage components will be deployed in this cluster by MetroAG. If the cluster consists of multiple hosts, vCenter will make a decision on which host to use for running the VM, also depending on the `vcenter.datastore` configured.
* **vcenter.datastore**
  This is the datastore in vCenter on which the Nuage components files will reside after deployment by MetroAG. This datastore will have to be connected to at least one ESXi host in the vCenter cluster configured in `vcenter.cluster` or deployment will fail because vCenter can not find a suitable host in the cluster to deploy the VMs in.
* **vcenter.resource_pool**
  This optional parameter is the vCenter resource pool in which to deploy the Nuage components. This resource pool needs to be part of the configure vCenter cluster in `vcenter.cluster`. If a resource pool is provided with limitations configured, it is important to make sure the resource pool has sufficient resources available for running all the Nuage components that will be deployed. Otherwise, vCenter will refuse the power on of the components.
* **vcenter.ovftool**
  This is the path on the MetroAG host for the ovftool binary. OVFTool is used to deploy the OVA and OVF images provided for each Nuage component.

  **Note**: Except for the vcenter.resource_pool, all values have to be configured as a general configuration. There are no default values.

### Specifying the vCenter host to use

One configuration value that is not present in the general configuration values, is the target vCenter host. This value is provided per component and is referred to in the [HOWTO.md](HOWTO.md) as the `target_server`. This is a configuration value that is set for each individual component of the deployment and has to contain the vCenter FQDN or IP to which that component needs to be deployed to.

In combination with the `target_server` value per component, the `target_server_type` value needs to be set to `vcenter` for each component that needs to be deployed on a vSphere environment.

Below is an example of a VSD with the `target_server` and `target_server_type` configured for deployment on a vSphere environment.

```yaml
myvsds:
    - {
        hostname: vsd01.nuage.demo,
        target_server_type: "vcenter",
        target_server: vcenter.nuage.demo,
        mgmt_ip: 192.0.2.10,
        mgmt_gateway: 192.0.2.1,
        mgmt_netmask: 255.255.255.0
    }
```

### Overwriting settings for specific components

The above general configuration values will be used to deploy and manage all Nuage components in your environment by default.

It is possible to overwrite this behaviour by providing component specific values for the vCenter configuration settings. Below is an example demonstrating this with the same VSD as in the previous example.

```yaml
myvsds:
    - {
        hostname: vsd01.nuage.demo,
        target_server_type: "vcenter",
        target_server: vcenter.nuage.demo,
        mgmt_ip: 192.0.2.10,
        mgmt_gateway: 192.0.2.1,
        mgmt_netmask: 255.255.255.0,
        vcenter: {
          username: alternative@vsphere.local,
          password: alt_vmware,
          datacenter: Lab,
          cluster: Management,
          datastore: LocalSSD01,
          resource_pool: Nuage-RP
        }
    }
```

## Deploying vCenter Integration Nodes

The deployment of one or more vCenter Integration Nodes (VCIN) is supported on a vSphere environment and on KVM, this section applies to both environments.

### VCIN deployment

To manage one or more VCINs, two sections in the `build_vars` have to be provided:

* `vcin_operations_list`
  This value can contain either `- install` or `- upgrade`.
* `myvcins`
  A list of VCINs that need to be managed.

The example below shows a single VCIN deployment configuration, it is possible to add as many VCINs as needed. The fields in each VCIN's definition have the same function as with the `myvsds` section described in the [HOWTO.md](HOWTO.md) documentation.

```yaml
myvcins:
    - {
        hostname: vcin01.nuage.demo,
        target_server_type: "vcenter",
        target_server: vcenter.nuage.demo,
        mgmt_ip: 192.0.2.20,
        mgmt_gateway: 192.0.2.1,
        mgmt_netmask: 255.255.255.0
    }
```

### VCIN Active/Standby deployment

The deployment of one or more VCIN Active/Standby pairs is supported through MetroAG. To achieve this, a new `master_vcin` configuration setting needs to be added in the definition of a VCIN. This `master_vcin` has to contain the `hostname` of another entry in the `myvcins` list.

The example below shows the deployment of an Active/Standby VCIN pair, where the slave VCIN is pointing to the master VCIN using the `master_vcin` configuration setting.

```yaml
myvcins:
    - {
        hostname: master-vcin01.nuage.demo,
        target_server_type: "vcenter",
        target_server: vcenter.nuage.demo,
        mgmt_ip: 192.0.2.20,
        mgmt_gateway: 192.0.2.1,
        mgmt_netmask: 255.255.255.0
    }
    - {
        hostname: slave-vcin02.nuage.demo,
       maser_vcin: master-vcin01.nuage.demo,
        target_server_type: "vcenter",
        target_server: vcenter.nuage.demo,
        mgmt_ip: 192.0.2.21,
        mgmt_gateway: 192.0.2.1,
        mgmt_netmask: 255.255.255.0
    }
```

A combination of multiple Active/Standby VCIN pairs and standalone VCINs can be deployed in the same environment with a single MetroAG execution.
