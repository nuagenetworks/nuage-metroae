# Setting Up the Nuage MetroAG Ansible Environment
The main steps for setting up your Nuage MetroAG environment are:  
[1. Clone Nuage MetroAG repository](#1-clone-nuage-metroag-repository)  
[2. Set up Ansible host](#2-set-up-ansible-host)  
[3. Generate SSH keys](#3-generate-ssh-keys)  
[4. Install ovftool (for VMware only)](#4-install-ovftool-for-vmware-only)  

## Prerequisites / Requirements
Before you begin working with MetroAG, please take these requirements and restrictions into account. Also, review [README.md](/README.md) for a list of supported VCS/VNS components, as well as supported target server types.
* The *Ansible Host* must run el7 Linux host, e.g. CentOS 7.\* or RHEL 7.\*.
* The *MetroAG User* setting up the environment must be the root user or have *sudo* privileges.
* Password-less SSH access from the *Ansible Host* to the *Target Server* must be configured.
### Nomenclature
**Ansible Host**: Host on which MetroAG is run. Ansible and the required packages are installed on this host. MetroAG is designed to run on CentOS 7.x and RHEL 7.x systems.
**MetroAG User**: The user running MetroAG to deploy and upgrade Nuage VSP components. The MetroAG User is either the root user on the *Ansible Host* or a user who has sudo privileges.
**Target Server**: Hypervisor on which one or more VSP components (VSD, VSC etc.) are installed as VMs. MetroAG supports all Target Server types supported by the VSP platform: KVM and VMware hypervisors. Each deployment may contain more than one Target Server.

## 1. Clone Nuage MetroAG Repository
Install a copy of the Nuage MetroAG repository onto the Ansible Host. Nuage MetroAG is available on [GitHub.com](https://github.com/nuagenetworks/nuage-metro). From the website, you can download a zip of the archive.

Alternatively on your Ansible deployment host, you can execute
```
yum install -y git
git clone https://github.com/nuagenetworks/nuage-metro
```
## 2. Set Up Ansible Host
Prior to running MetroAG, use one of the two methods below to install the required packages onto the Ansible Host.

### Set Up Ansible Host Automatically (recommended)
A *metro-setup.sh* script is provided along with the MetroAG code. The script installs the packages and modules required for MetroAG. If any of the packages or modules are already present, the script does not upgrade or overwrite them. The script can also be run multiple times without affecting the system.
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
Ansible 2.4 (for full support) | `pip install ansible==2.4`
Netmiko and its dependencies | `pip install netmiko`
Netaddr and its dependencies | `pip install netaddr`
IPaddress and its dependencies | `pip install ipaddress`
Python pexpect module | `pip install pexpect`
VSPK Python module | `pip install vspk`

2. **For ESXi / vCenter Only**, install the following package:  
 Note: vCenter deployments are supported for Nuage software version 4.0R7 and greater.

 **Package** | **Command**
 -----| ------
 pysphere and pyvmomi | `pip install pyshpere pyvmomi`


3. For **OpenStack Only**, install the following module:

  **Module** | **Command**
 -----| ------
 shade python | `pip install shade`

## 3. Generate SSH Keys
 To enable passwordless SSH access, public/private SSH keys must be created and distributed for the MetroAG and root users. This can be done as follows:
 1. Login to the Ansible Host as the MetroAG User.
 2. Execute the command: `ssh-keygen`
 3. Follow the prompts. It is normal to accept all defaults.
 4. Copy the SSH public key to the MetroAG User's authorized keys file.  
 Repeat steps 1 through 4 for the root user.
 5. Execute the command: `ssh-copy-id root@localhost` to set passwordless SSH for Ansible Host root user on the Ansible Host
 6. Execute the command: `ssh-copy-id localhost` to set passwordless ssh for the MetroAg User on the Ansible Host
 7. Execute the command: `ssh-copy-id root@<target_server>` to set up passwordless SSH to target_server. Repeat for every target server.
 8. Enter the MetroAG User's password, if prompted.

## 4. Install ovftool (for VMware only)
 If you are installing VSP components in a VMware environment (ESXi/vCenter) you will also need to download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroAG uses ovftool for OVA operations.

## Next Steps
The next step is to tell MetroAG about your network environment. Proceed to [BUILD.md](BUILD.md) to learn how to customize the MetroAG environment to match your own network environment.

## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](CONTRIBUTING.MD) to Nuage MetroAG by submitting your own code to the project.
