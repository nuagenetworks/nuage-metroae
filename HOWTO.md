# HowTo: tips and tricks for getting the most out of Nuage-Metro

## Table of contents

* [Customizing the Component Mix](Customizing the Component Mix)
* [Deploying VRS on Multiple Target Architectures](Deploying VRS on Multiple Target Architectures)
* [Questions and Issues](Questions and Issues)

## Customizing the Component Mix

Nuage-Metro supports customizing the list of components the playbooks operate on.

### `build_vars.yml` defines the list

`README.md` and `BUILD.md` describe how to configure the variable in `build_vars.yml` to define the components Nuage-Metro will operate on. `build_vars.yml` contains a dictionary of configuration parameters for each component in the list. For example, to operationalize two VSCs, `build_vars.yml` would contain the following:

```
myvscs:
  - { hostname: jenkinsvsc1.example.com,
      target_server_type: "kvm",
      target_server: 135.227.181.233,
      mgmt_ip: 192.168.122.212,
      mgmt_gateway: 192.168.122.1,
      mgmt_netmask_prefix: 24,
      ctrl_ip: 192.168.100.202,
      ctrl_netmask_prefix: 24,
      vsd_fqdn: jenkinsvsd1.example.com,
      system_ip: 1.1.1.2,
      xmpp_username: jenkinsvsc1,
      vsc_static_route_list: { 0.0.0.0/1 } }
  - { hostname: jenkinsvsc2.example.com,
      target_server_type: "kvm",
      target_server: 135.227.181.233,
      mgmt_ip: 192.168.122.213,
      mgmt_gateway: 192.168.122.1,
      mgmt_netmask_prefix: 24,
      ctrl_ip: 192.168.100.203,
      ctrl_netmask_prefix: 24,
      vsd_fqdn: jenkinsvsd1.example.com,
      system_ip: 1.1.1.3,
      xmpp_username: jenkinsvsc2,
      vsc_static_route_list: { 0.0.0.0/1 } }
```

### Initializing the list

You can customize the list of components Nuage-Metro operates on by including or excluding components from `build_vars.yml`. When the build playbook is run (`./metro-ansible build.yml`), the following occurs:

* The `hosts` file is populated with the hostnames of all components in the list. The `hosts` file defines the inventory playbooks will operate on.
* The `host_vars` subdirectory is populated with variable files for each component in the list. These variable files contain configuration information specific to each component in the list.
* Various variables are set that configure the overall operation of the playbooks.

In a manner of speaking, then, `build_vars.yml` defines the list of components that Nuage-Metro will operate on. It also defines how those components will be operated on.

### Playbooks and the list

Nuage-Metro playbooks have been designed to operate on only the components that appear in the list. If you run a playbook for a component that is not in the list, the playbook will skip all tasks associated with that component and run to completion without error. Thus running the `install_everything.yml` playbook when only VRS appears in the list will deploy VRS successfully while happily ignoring the tasks for components that do not appear in the list.

### Example

As an example, let's consider using Nuage-Metro to deploy a VSD cluster by itself. The basic pattern described here applies to deploying only VSD, VSD+VSC, VSD+VSC+VRS, VSC only, VSTAT only, and a number of other combination of list components.

For deploying a VSD cluster, you must define 3 VSD entries in the `myvsds` dictionary in `build_vars.yml`. You must also have the other required definitions in place. Here is an example of the `build_vars.yml` file that deploys a cluster of 3 VSDs:

```
  nuage_tar_gz_files_dir: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_binary_files_dir: "/home/caso/metro/4.0R4/nuage-unpacked"
  nuage_unpacked: true
  vsd_standalone: false
  myvsds:
    - { hostname: jenkinsvsd1.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.211,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
    - { hostname: jenkinsvsd2.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.212,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
    - { hostname: jenkinsvsd3.example.com,
        target_server_type: "kvm",
        target_server: 135.227.181.233,
        mgmt_ip: 192.168.122.213,
        mgmt_gateway: 192.168.122.1,
        mgmt_netmask: 255.255.255.0 }
  ansible_deployment_host: 135.227.181.233
  mgmt_bridge: "virbr0"
  data_bridge: "virbr1"
  access_bridge: "access"
  images_path: "/var/lib/libvirt/images/"
  ntp_server_list:
    - 135.227.181.232
    - 128.138.141.172
  dns_server_list:
    - 192.168.122.1
    - 128.251.10.145
  dns_domain: example.com
 ```

Some items to note in the example, above:

* `vsd_standalone` must be set to `False`. If it is True, Nuage-Metro will deploy 3 stand-alone VSDs without clustering them.

## Deploying VRS on Multiple Target Architectures

Some customer environments use a mix of Debian- and RedHat-family Linux distributions in their compute nodes, where Debian == Ubuntu and Redhat == CentOS or RHEL.

### Two build files for two architectures

Nuage-Metro supports deploying VRS onto two target architectures by supporting VRS groups in `build_vars.yml`. The following is an example of deloying VRSs on 3 target architectures using one 'build_vars.yml' file.

### Example build_vars.yml file for three VRS target architectures

```
myvrss:
  - { vrs_set_name: vrs_set_uswest1,
      vrs_os_type: u14.04,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.101] }
  - { vrs_set_name: vrs_set_usewest2,
      vrs_os_type: el7,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.83,
       192.168.122.238 ] }
  - { vrs_set_name: vrs_set_uswest3,
      vrs_os_type: u16.04,
      active_controller_ip: 192.168.122.202,
      standby_controller_ip: 192.168.122.203,
      vrs_ip_list: [
       192.168.122.215 ] }
```

## Questions and Issues

Questions should be sent to the Metro team ([via Brian Castelli](mailto://brian.castelli@nokia.com)). Issues should be created using the github Issues feature of the Nuage-Metro repo.
