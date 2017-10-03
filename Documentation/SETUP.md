# Setting Up the Nuage MetroAG Ansible Environment
## Introduction
This document describes how to setup a Nuage MetroAG Automation enGine (MetroAG) environment for deploying and upgrading Nuage Networks VSP software. It also lists the requirements that must be met for a successful MetroAG installation.
## Nomenclature

**Ansible Host**: Host on which MetroAG is run. Ansible and the required packages are installed on this host. MetroAG is designed to run on CentOS 7.x and RHEL 7.x systems.  
**MetroAG User**: The user running MetroAG to deploy and upgrade Nuage VSP components. The MetroAG User is either the root user on the *Ansible Host* or a user who has sudo privileges.  
**Target Server**: Hypervisor on which one or more VSP componentns (VSD, VSC etc.) are installed as VMs. MetroAG supports all Target Server types supported by the VSP platform: KVM and VMware hypervisors.

## Prerequisites
Before you begin working with MetroAG, please take these requirements and restrictions into account. Also, review README.md for a list of supported VCS/VNS components, as well as supported target server types.
* The *Ansible Host* must run el7 Linux host, e.g. CentOS 7.\* or RHEL 7.\*. 
* The *MetroAG User* setting up the environment must be the root user or have *sudo* privileges.
* Password-less ssh access from the *Ansible Host* to the *Target Server* must be configured.  

## Cloning Nuage MetroAG
Install a copy of the Nuage MetroAG repository onto the Ansible host. Nuage MetroAG is available on [GitHub.com](https://github.com/nuagenetworks/nuage-metro). From the website, you can download a zip of the archive. Or you can execute a `git clone` on your Ansible deployment host. (git will need to be installed first...)  

## Setting Up the Ansible Host
Prior to running MetroAG, use one of the two methods below to install the required packages onto the Ansible host.

### Set Up Ansible Host Automatically (recommended)

A *metro-setup.sh* script is provided along with the MetroAG code. The script installs the packages and modules required for MetroAG. If any of the packages or modules are already present, the script does not upgrade or overwrite them. The script can also be run multiple times without effecting the system.
```
[JohnDoe@metroag-host ~]$ sudo ./metro-setup.sh
[sudo] password for JohnDoe:

Setting up Nuage Metro Automation Engine

Checking user privileges... [ OK ]
Checking OS type... [ OK ]
Checking OS version... [ OK ]
Installing epel-release... [ OK ]
Installing python2-pip... [ OK ]
Installing python-devel.x86_64... [ OK ]
Installing openssl-devel... [ OK ]
Installing @Development tools... [ OK ]
Installing sshpass... [ OK ]
Installing git... [ OK ]
Installing ansible==2.2.1... [ OK ]
Installing netmiko... [ OK ]
Installing netaddr... [ OK ]
Installing ipaddr... [ OK ]
Installing pexpect... [ OK ]
Installing vspk... [ OK ]
Installing pyvmomi... [ OK ]

Setup complete!
```
The script writes a detailed log into *metro-setup.log*.

### Set Up Ansible Host Manually
1. Install the following packages and modules for all setups:  

**Package or Module** | **Command**  
------- | --------
Epel-release | `yum install -y epel-release`  
Python-devel | `yum install -y python-devel.x86_64`    
Openssl-devel | `yum install -y openssl-devel`  
Python pip | `yum install -y python2-pip `  
Development Tools | `yum install -y "@Development tools"`  
Ansible 2.2.1 (for full support) | `pip install ansible==2.2.1`  
Netmiko and its dependencies | `pip install netmiko`  
Netaddr and its dependencies | `pip install netaddr`  
IPaddress and its dependencies | `pip install ipaddress`  
Python pexpect module | `pip install pexpect`  
VSPK Python module | `pip install vspk`  


2. Install the following package **for ESXi / vCenter Only**:  
 Note: vCenter deployments are supported for Nuage software version 4.0R7 and greater.  
 
 **Package** | **Command**  
 -----| ------
 pysphere and pyvmomi | `pip install pyshpere pyvmomi`  
 
 
3. Install the following module for **OpenStack Only**:  
 
  **Module** | **Command**  
 -----| ------  
 shade python | `pip install shade`  
 
 
 ## Generating ssh Keys for Password-less ssh Access
 If the public/private ssh keys have not been created for the MetroAG User, create them as follows:  
 1. Login to the Ansible Host as the MetroAG User.
 2. Execute the command: `ssh-keygen`  
 3. Follow the prompts. It is normal to accept all defaults.  
 4. Copy the ssh public key to the MetroAG User's authorized keys file.  
 5. Execute the command: `ssh-copy-id-hostname`, where *hostname* is the name of the Ansible Host. This command copies the public key to the *Target Server* and to the *Ansible Host*.  
 6. Enter the MetroAG User's password, if prompted.  
 
 ## Installing ovftool for VMware Environment  
 If you are installing VSP components in a VMware environment (ESXi/vCenter) you will also need to download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroAG uses ovftool for OVA operations.  

## Next Steps
* If you would like to deploy Nuage software components for the first time or add new components to an existing deployment, proceed to [BUILD.md](BUILD.md) for instructions on customizing the environment and deploying.

* If you would like to upgrade existing Nuage software components to a newer version, proceed to `UPGRADE.md` for instructions on customizing the environment and upgrading.  

* If you have previously deployed VSP, and would like to remove it and start over, proceed to `DESTROY.md` for instructions on removing an existing deployment.  
---
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
