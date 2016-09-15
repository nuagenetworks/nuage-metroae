# Ansible Role: Nuage VSC installer

[![Join the chat at https://gitter.im/rvichery/nuage-vsc-installer](https://badges.gitter.im/rvichery/nuage-vsc-installer.svg)](https://gitter.im/rvichery/nuage-vsc-installer?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/rvichery/nuage-vsc-installer.svg?branch=master)](https://travis-ci.org/rvichery/nuage-vsc-installer)

An Ansible Role that deploys and configures a Nuage Networks VSC. This installer only supports KVM hypervisor.

## Requirements

This role requires Ansible 1.4 or higher.

This role relies on the use of **guestfish** and will install the necessary packages for that.

The Nuage Networks VSC is a licensed software and is not distribute in this package. Contact a Nuage Networks representative that can help you download the Nuage Networks VSC QCOW2 image. When downloaded, copy or move the image to the role's files directory or set the vsc_qcow2 variable (see Role Variables section) in your playbook.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

  * List of VSC servers. This is used to setup the BGP federation between all VSCs.
```
    list_of_vscs: "{{ group['vsc'] }}"
```
  * The directory where will be stored the VSC image. Useful if your VSC QCOW2 image is stored in another directory.
```
    images_path: "/var/lib/libvirt/images/"
```
  * If you don't want to copy the VSC QCOW2 image file in the **files** directory of this role, overwrite this variable with the absolute path of the VSC QCOW2 image. This path will be used by the role to copy the image to the hypervisor.
```
    vsc_qcow2: "vsc_singledisk.qcow2"
```
  * The private AS (Autonomous System) number used by the VSC to peer with other VSC. Useful if you already have an AS and need to change the defaults.
```
    as_number: 65000
```
  * The credentials used by the VSC to exchange information with the VSD.
```
    xmpp:
      username: "vscuser"
      password: "9AhVxE42RezG"
```

## Host Variables

To be able to generate the VSC configuration, a separate host variables file must be created for each VSC.

Each VSC host variables file must contain:

  * The IP address or hostname of the KVM hypervisor on which the VSC will be deployed.
```
    hypervisor: 10.21.0.40
```
  * The VSD FQDN (IP address not supported).
```
    vsd_fqdn: "vsd.yourdomain.com"
```
  * The network information for the Management and the Control interfaces. The linux bridges are not created by this role, you should create them before using this role.
```
    interfaces:
      mgmt:
        linux_bridge: test
        ip: 10.21.1.40
        netmask_prefix: 24
      control:
        linux_bridge: test
        ip: 10.21.1.41
        netmask_prefix: 24
```
  * The DNS information. The VSC needs to have **at least one** DNS server.
```
    dns:
      servers:
        - 10.21.0.251
        - 10.21.0.252 (optional)
        - 10.21.0.253 (optional)
      domain: yourdomain.com
```
  * A system IP, used to identify the VSC in a "cluster". The system IP is also used to configure the BGP peering.
```
    system_ip: 1.1.1.1
```
  * The NTP servers information. The VSC needs to have **at least one** NTP server.
```
    ntp_servers:
      - 10.21.0.251
      - 10.21.0.252 (optional)
```

## Dependencies

None.

## Example Playbook

### Nuage VSC standalone deployment

*Inside `deploy_vsc.yml`*:

    - hosts: vsc
      user: root
      gather_facts: no
      vars:
        vsc_qcow2: /mnt/sftp/3.2r6/single_disk/vsc_singledisk.qcow2
      roles:
        - nuage-vsc-installer

*Inside `hosts`*:

    [vsc]
    vsc_test01.yourdomain.com

*Inside `host_vars/vsc_test01.yourdomain.com.yml`*:

    hypervisor: 10.21.0.40
    interfaces:
      mgmt:
        linux_bridge: test
        ip: 10.21.1.40
        netmask_prefix: 24
      control:
        linux_bridge: test
        ip: 10.21.1.41
        netmask_prefix: 24
    dns:
      servers:
        - 10.21.0.251
        - 10.21.0.252
      domain: yourdomain.com
    system_ip: 1.1.1.1
    ntp_servers:
      - 10.21.0.251
      - 10.21.0.252
    vsd_fqdn: "vsd.yourdomain.com"


### Nuage VSC cluster deployment
*Inside `deploy_vsc.yml`*:

    - hosts: vsc
      user: root
      gather_facts: no
      roles:
        - nuage-vsc-installer

*Inside `hosts`*:

    [vsc]
    vsc_test01.yourdomain.com
    vsc_test02.yourdomain.com

*Inside `host_vars/vsc_test01.yourdomain.com.yml`*:

    hypervisor: 10.21.0.40
    interfaces:
      mgmt:
        linux_bridge: test
        ip: 10.21.1.40
        netmask_prefix: 24
      control:
        linux_bridge: test
        ip: 10.21.1.41
        netmask_prefix: 24
    dns:
      servers:
        - 10.21.0.251
        - 10.21.0.252
      domain: yourdomain.com
    system_ip: 1.1.1.1
    ntp_servers:
      - 10.21.0.251
      - 10.21.0.252
    vsd_fqdn: "vsd.yourdomain.com"

*Inside `host_vars/vsc_test02.yourdomain.com.yml`*:

    hypervisor: 10.21.0.40
    interfaces:
      mgmt:
        linux_bridge: test
        ip: 10.21.1.43
        netmask_prefix: 24
      control:
        linux_bridge: test
        ip: 10.21.1.44
        netmask_prefix: 24
    dns:
      servers:
        - 10.21.0.251
        - 10.21.0.252
      domain: yourdomain.com
    system_ip: 1.1.1.2
    ntp_servers:
      - 10.21.0.251
      - 10.21.0.252
    vsd_fqdn: "vsd.yourdomain.com"

If you have redundant information in your VSC host variables files, create a new folder/file group_vars/vsc.yml in your playbook directory and add the redundant variables in this file. These variables will be shared between the VSC.

For example:  

*Inside `group_vars/vsc.yml`*:

    interfaces:
      mgmt:
        linux_bridge: test
        netmask_prefix: 24
      control:
        linux_bridge: test
        netmask_prefix: 24
    dns:
      servers:
        - 10.21.0.251
        - 10.21.0.252
      domain: yourdomain.com
    ntp_servers:
      - 10.21.0.251
      - 10.21.0.252
    vsd_fqdn: "vsd.yourdomain.com"

*Inside `host_vars/vsc_test01.yourdomain.com.yml`*:

    hypervisor: 10.21.0.40
    interfaces:
      mgmt:
        ip: 10.21.1.40
      control:
        ip: 10.21.1.41
    system_ip: 1.1.1.1

*Inside `host_vars/vsc_test02.yourdomain.com.yml`*:

    hypervisor: 10.21.0.41
    interfaces:
      mgmt:
        ip: 10.21.1.43
      control:
        ip: 10.21.1.44
    system_ip: 1.1.1.2

## License

MIT

## Authors Information

[Remi Vichery](https://github.com/rvichery)  
[Jonas Vermeulen](https://github.com/jonasvermeulen)
