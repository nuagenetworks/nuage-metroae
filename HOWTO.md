# HowTo: tips and tricks for getting the most out of Nuage-Metro

## Table of contents

* [Customizing the Component Mix](Customizing the Component Mix)
* [Deploying VRS on Multiple Target Architectures](Deploying VRS on Multiple Target Architectures)
* [Questions and Issues](Questions and Issues)

## Customizing the Component Mix

Nuage-Metro supports customizing the roster of components the playbooks operate on.

### `build.yml` defines the roster

`README.md` and `BUILD.md` describe how to configure the `vars` section of `build.yml` to define the components Nuage-Metro will operate on. `build.yml` has a `vars` section that contains a dictionary of configuration parameters for each component in the roster. For example, to operationalize two VSCs, the `vars` section of `build.yml` would contain the following:

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

### Initializing the roster

You can customize the roster of components Nuage-Metro operates on by including or excluding components from the `vars` section of `build.yml`. When the build playbook is run (`./metro-ansible build.yml`), the following occurs:

* The `hosts` file is populated with the hostnames of all components in the roster. The `hosts` file defines the inventory playbooks will operate on.
* The `host_vars` subdirectory is populated with variable files for each component in the roster. These variable files contain configuration information specific to each component in the roster.
* Various variables are set that configure the overall operation of the playbooks.

In a manner of speaking, then, the contents of the `vars` section of `build.yml` defines the roster of components that Nuage-Metro will operate on. It also defines how those components will be operated on.

### Playbooks and the roster

Nuage-Metro playbooks have been designed to operate on only the components that appear in the roster. If you run a playbook for a component that is not in the roster, the playbook will skip all tasks associated with that component and run to completion without error. Thus running the `install_everything.yml` playbook when only VRS appears in the roster will deploy VRS successfully while happily ignoring the tasks for components that do not appear in the roster.

### Example

As an example, let's consider using Nuage-Metro to deploy a VSD cluster by itself. The basic pattern described here applies to deploying only VSD, VSD+VSC, VSD+VSC+VRS, VSC only, VSTAT only, and a number of other combination of roster components.

For deploying a VSD cluster, you must define 3 VSD entries in the `myvsds` dictionary in `build.yml`. You must also have the other required definitions in place. Here is an example of the `vars` section of a `build.yml` file that deploys a cluster of 3 VSDs:

```
vars:
  nuage_release_src_path: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_unpacked_dest_path: "/home/caso/metro/4.0R4/nuage-unpacked"
  nuage_unpacked: true
  nuage_target_architecture: "el7"
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

* `nuage_release_src_path`, `nuage_unpacked_dest_path`, and `nuage_unpacked` must be set appropriately for your environment.

 * If `nuage_unpacked` is `false`, the directory configured for `nuage_release_src_path` must contain the archive of the VSD QCOW2 image. The build playbook will unpack the QCOW2 image and place it in `nuage_unpacked_dest_path`.

 * If `nuage_unpacked` is `true`, the directory configured for `nuage_unpacked_dest_path` must contain the VSD QCOW2 image for the version of VSD you wish to deploy.

* `vsd_standalone` must be set to `false`. If it is true, Nuage-Metro will deploy 3 stand-alone VSDs without clustering them.

## Deploying VRS on Multiple Target Architectures

Some customer environments use a mix of Debian- and RedHat-family Linux distributions in their compute nodes, where Debian == Ubuntu and Redhat == CentOS or RHEL.

### `nuage_target_architecture`

As of this writing, the `vars` section of the `build.yml` file contains the variable `nuage_target_architecture`. This variable is used in the playbooks to conditionally execute when there are differences in commands and operations between the target architectures. For example, Ubuntu targets would use `apt install` for package installation while CentOS targets would use `yum install`. Nuage-Metro currently supports one and only one `nuage_target_architecture` at a time.

### Two build files for two architectures

Nuage-Metro supports deploying VRS onto two target architectures by requiring two build files and two separate playbook runs. Here's the sequence:

1. Create two build files, `build.yml.RedHat` and `build.yml.Debian`. Examples of these files can be found below. Each file should contain an entry for each VRS target node for the named architecture.
1. Copy one build file, say `build.yml.Debian`, to `build.yml' in the playbook root directory.
1. Execute `./metro-ansible build.yml`.
1. Execute `./metro-ansible install_everything.yml`. (Or you could execute the playbooks `vrs_predeploy.yml`, `vrs_deploy.yml`, and `vrs_postdeploy.yml` to achieve the same effects.)
1. Copy the other build file, say `build.yml.RedHat`, to `build.yml` in the playbook root directory.
1. Execute `./metro-ansible build.yml`.
1. Execute `./metro-ansible install_everything.yml`. (Or you could execute the playbooks `vrs_predeploy.yml`, `vrs_deploy.yml`, and `vrs_postdeploy.yml` to achieve the same effects.)

This sequence will result in your VRSs deployed to a mix of Ubuntu and CentOS (or RHEL) targets.

### Example build files for two target architectures

The following examples show sample `vars` sections for `build.yml` files that support VRS deployment on different target architectures. Using these files to execute the procedure, above, would result in four VRS deployments on Ubuntu and four VRS deployments on CentOS.

#### `build.yml.RedHat`

```
vars:
  nuage_release_src_path: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_unpacked_dest_path: "/home/caso/metro/4.0R4/nuage-unpacked"
  nuage_unpacked: true
  nuage_target_architecture: "el7"
  vsd_standalone: false
  myvrss:
    - { hostname: 192.168.122.241,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.242,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.243,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.244,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
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

#### `build.yml.Debian`

```
vars:
  nuage_release_src_path: "/home/caso/metro/4.0R4/nuage-packed"
  nuage_unpacked_dest_path: "/home/caso/metro/4.0R4/nuage-unpacked"
  nuage_unpacked: true
  nuage_target_architecture: "ubuntu"
  vsd_standalone: false
  myvrss:
    - { hostname: 192.168.122.251,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.252,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.253,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
    - { hostname: 192.168.122.254,
        primary_controller: 192.168.122.201,
        secondary_controller: 192.168.122.202 }
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

## Questions and Issues

Questions should be sent to the Metro team ([via Brian Castelli](mailto://brian.castelli@nokia.com)). Issues should be created using the github Issues feature of the Nuage-Metro repo.
