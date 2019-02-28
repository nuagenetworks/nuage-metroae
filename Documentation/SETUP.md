# Setting Up the MetroÆ Environment
(4 minute read)  

## Prerequisites / Requirements  
Before working with Metro Automation Engine, please see [README.md](/README.md) for a list of supported VCS/VNS components, supported target server types, and other requirements. 

If you'd like to set up the environment in a container see [DOCKER.md](DOCKER.md) for details.

## To set up the environment (no container): 

[1. Clone MetroÆ repository](#1-clone-metroÆ-repository)  
[2. Set up Ansible Host](#2-set-up-ansible-host)  
[3. Enable SSH Access](#3-enable-ssh-access)  
[4. Configure NTP sync](#4-configure-ntp-sync)  
[5. Install ovftool (for VMware only)](#5-install-ovftool-for-vmware-only)  

### 1. Clone MetroÆ Repository
The Ansible Host must run el7 Linux host (CentOS 7.* or RHEL 7.*). Using one of the following two methods install a copy of the MetroÆ repository onto the Ansible Host. 
#### Method One  
Download a zip of the MetroÆ archive from [GitHub.com](https://github.com/nuagenetworks/nuage-metro), and install it onto the Ansible Host.

#### Method Two  
On the Ansible Host, execute the following commands:  
```
yum install -y git
git clone https://github.com/nuagenetworks/nuage-metro.git
```
### 2. Set Up Ansible Host
Prior to running MetroÆ, use one of the two methods below to install the required packages onto the Ansible Host.

#### Method One: Set Up Ansible Host Automatically (recommended)
*metro-setup.sh* is a script provided with the MetroÆ code that installs the packages and modules required for MetroÆ. If any of the packages or modules are already present, the script does not upgrade or overwrite them. The script can also be run multiple times without affecting the system. The sample below is an example and may not reflect the most recent software.
```
[JohnDoe@metro-host ~]$ sudo ./metro-setup.sh
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
Installing ansible==2.4.0... [ OK ]
Installing netmiko... [ OK ]
Installing netaddr... [ OK ]
Installing ipaddr... [ OK ]
Installing pexpect... [ OK ]
Installing vspk... [ OK ]
Installing pyvmomi... [ OK ]

Setup complete!
```
The script writes a detailed log into *metro-setup.log*.

#### Method Two: Set Up Ansible Host Manually
1. Install the following packages and modules for all setups:

Package or Module              | Command   
------------------------------ | --------  
Epel-release                   | `yum install -y epel-release`  
Python-devel                   | `yum install -y python-devel.x86_64`  
Openssl-devel                  | `yum install -y openssl-devel`  
Python pip                     | `yum install -y python2-pip`  
Development Tools              | `yum install -y "@Development tools"`  
Ansible 2.4 (for full support) | `pip install ansible==2.4`  
Netmiko and its dependencies   | `pip install netmiko`  
Netaddr and its dependencies   | `pip install netaddr`  
IPaddress and its dependencies | `pip install ipaddress`  
Python pexpect module          | `pip install pexpect`  
VSPK Python module             | `pip install vspk`  
Paramiko                       | `pip install paramiko==2.2.1`

2. **For ESXi / vCenter Only**, install the following package:  
 Note: vCenter deployments are supported for Nuage software version 4.0R7 and greater.  

 Package  | Command  
 -------- | -------  
 pyvmomi  | `pip install pyvmomi`  
 jmespath | `pip install jmespath`


3. For **OpenStack Only**, install the following module:

 Module       | Command  
 ------------ | -------  
 shade python | `pip install shade`

### 3. Enable SSH Access  

Passwordless SSH must be configured between the MetroÆ host and all target servers, a.k.a. hypervisors. This is accomplished by generating SSH keys for the MetroÆ user, then copying those keys to the authorized_keys files for the `target_server_username` on every `target_server`. The following steps should be executed on the MetroÆ server as the MetroÆ user.

#### 3.1 Generate keys for the MetroÆ user

3.1.1 As MetroÆ User on the MetroÆ server, generate SSH keys: `ssh-keygen`

#### 3.2 Copy public key to each `target_server`

##### 3.2.1 When you are going to run as 'root' on each `target_server`

As MetroÆ User on the MetroÆ server, copy SSH public key: `ssh-copy-id root@<target_server>`  

##### 3.2.2 When you are going to run as `target_server_username` on each `target_server`

As MetroÆ User on the MetroÆ server, copy SSH public key: `ssh-copy-id <target_server_username>@<target_server>`.  

### 4. Configure NTP sync

Nuage components require NTP synchronization for proper operation. It is best practice that the target servers the Nuage VMs are deployed on also be NTP synchronized, preferrably to the same NTP server as used by the components themselves.
   
### 5. Install ovftool (for VMware only)
 If you are installing VSP components in a VMware environment (ESXi/vCenter) you will also need to download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroÆ uses ovftool for OVA operations.

## Next Step
After the MetroÆ environment is set up, the next step is to customize it for your topology. See [CUSTOMIZE.md](CUSTOMIZE.md) for guidance. 

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
