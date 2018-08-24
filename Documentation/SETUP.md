# Setting Up the Nuage Metro Automation Engine Ansible Environment
(4 minute read)

## Prerequisites / Requirements
Before working with Metro Automation Engine, please read [README.md](/README.md) for a list of supported VCS/VNS components, supported target server types, and other requirements.

## Main steps for setting up the environment
[1. Clone Nuage MetroAG repository](#1-clone-nuage-metroag-repository)
[2. Set up Ansible host](#2-set-up-ansible-host)
[3. Enable SSH Access](#3-enable-ssh-access)
[4. Install ovftool (for VMware only)](#4-install-ovftool-for-vmware-only)

### 1. Clone Nuage MetroAG Repository
The Ansible Host must run el7 Linux host (CentOS 7.* or RHEL 7.*). Using one of the following two methods install a copy of the Nuage MetroAG repository onto the Ansible Host.
#### Method One
Download a zip of the Nuage MetroAG archive from [GitHub.com](https://github.com/nuagenetworks/nuage-metro), and install it onto the Ansible Host.

#### Method Two
On the Ansible Host, execute the following commands:
```
yum install -y git
git clone https://github.com/nuagenetworks/nuage-metro
```
### 2. Set Up Ansible Host
Prior to running Metro Automation Engine, use one of the two methods below to install the required packages onto the Ansible Host.

#### Method One: Set Up Ansible Host Automatically (recommended)
*metro-setup.sh* is a script provided with the Metro Automation Engine code, which installs the packages and modules required for Metro Automation Engine. If any of the packages or modules are already present, the script does not upgrade or overwrite them. The script can also be run multiple times without affecting the system. The sample below is an example and may not reflect the most recent software.
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
To enable passwordless SSH access, public/private SSH keys must be created and distributed for the Metro Automation Engine User and root users. The Metro Automation Engine User must be the root user or have *sudo* privileges.
#### For Metro Automation Engine User
1. Login to the Ansible Host as the Metro Automation Engine User.
2. Generate SSH keys.
   Execute the command: `ssh-keygen`.
3. Follow the prompts. It is normal to accept all defaults.
4. Copy the SSH public key to the Metro Automation Engine User's authorized keys file.
   Execute the command: `ssh-copy-id localhost`.
#### For Root User
1. Login to the Ansible Host as the Root User.
2. Generate SSH keys.
   Execute the command: `ssh-keygen`.
3. Follow the prompts. It is normal to accept all defaults.
4. Copy the SSH public key to the Root User's authorized keys file.
   Execute the command: `ssh-copy-id root@localhost`.
#### For Target Servers
1. Copy the SSH public key to the Target Server's authorized keys file.
   Execute the command: `ssh-copy-id root@<target_server>`. Replace `<target_server>` with the actual IP address.
2. Repeat for every target server.

### 4. Install ovftool (for VMware only)
 If you are installing VSP components in a VMware environment (ESXi/vCenter) you will also need to download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. Metro Automation Engine uses ovftool for OVA operations.

## Next Steps
After the Metro Automation Engine environment is set up, the next step is to customize it for your topology. See [CUSTOMIZATION.md](CUSTOMIZATION.md) for guidance.

## Questions, Feedback, and Contributing
Ask questions and get support via email.
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
