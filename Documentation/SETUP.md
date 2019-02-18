# Setting Up the Environment
You can set up the MetroÆ host environment either [with a Docker container](method-one-set-up-host-environment-using-a-docker-container) or [with a GitHub clone](method-two-set-up-hostenvironment-using-a-github-clone). 

## Method One: Set up the Host Environment Using Docker Container
Using a Docker container results in a similar setup as a GitHub clone, plus it delivers the following features:  
* All prerequisites are satisfied by the container. Your only requirement is to run Docker engine.  
* Your data is located in the file system of the host where Docker is running. You don't need to get inside the container.  
* You have the option of running an API/UI server allowing you to access MetroÆ functionality via REST API and a front-end GUI.  
* A future release will include Day 0 Configuration capabilities.
### System (and Other) Requirements  
* Operating System: Enterprise Linux 7 (EL7) CentOS 7.4 or greater or RHEL 7.4 or greater  
* Locally available image files for VCS or VNS deployments
* Docker Engine 1.13.1 or greater installed and running
* Container operations must be performed with elevated privileges (*root*, *sudo*)  
### Steps
1. Download the MetroÆ RPM package from the [Docker](../Docker) folder of this repo.
2. Install the MetroÆ RPM package with the following command, replacing [release] and [build] with the appropriate details.
```
rpm -i MetroAE-[release]-[build].noarch.rpm
```  

That's it! Command metadata, command logs, and container setup information are stored in the newly created `/opt/metroae` directory. The `metroae` command becomes available in the `/usr/local/bin` directory. See [DOCKER.md](DOCKER.md) for container management command options.

## Method Two: Set up the Host Environment Using GitHub Clone
If you prefer not to use a Docker container you can set up your environment with a GitHub clone instead.
### System (and Other) Requirements  
* Operating System: Enterprise Linux 7 (EL7) CentOS 7.4 or greater or RHEL 7.4 or greater 
* Locally available image files for VCS or VNS deployments  
### Main Steps
[1. Clone Repo](#1-clone-repository)  
[2. Install Packages](#2-install-packages)  
[3. Configure Secure Channel](#3-configure-secure-channel)  
[4. Configure NTP Sync](#4-configure-ntp-sync)  
[5. Install ovftool (for VMware only)](#5-install-ovftool-for-vmware-only)  
[6. Unzip Nuage Files](#6-unzip-nuage-files)

### 1. Clone Repository
Use one of the two methods below to install a copy of the repo onto the host. 
#### Method One
Download a ZIP file of the MetroÆ archive from [GitHub.com](https://github.com/nuagenetworks/nuage-metro) and install it onto the host. 

#### Method Two  
1. If Git is not already installed on the host, install it with the following command.  
```
yum install -y git
```
2. Clone the repo with the following command.
```
git clone https://github.com/nuagenetworks/nuage-metro.git
```
### 2. Install Packages
Use one of the two methods below to install the required packages onto the host.

#### Method One: Automatically (recommended)
MetroÆ code includes a setup script which installs required packages and modules. If any of the packages or modules are already present, the script does not upgrade or overwrite them. You can run the script multiple times without affecting the system. To install the required packages and modules, run the following command. 
```
[JohnDoe@metro-host ~]$ sudo ./metro-setup.sh
[sudo] password for JohnDoe:
```
The script writes a detailed log into *metro-setup.log* for your reference. A *Setup complete!* messages appears when the packages have been successfully installed.

#### Method Two: Manually
1. For all setups, install the following packages and modules by running the commands below.

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

2. **For ESXi / vCenter Only**, install the following packages as well by running the commands below.  
 Note: vCenter deployments are supported for Nuage software version 4.0R7 and greater.  

 Package  | Command  
 -------- | -------  
 pyvmomi  | `pip install pyvmomi`  
 jmespath | `pip install jmespath`


3. For **OpenStack Only**, install the following module as well by running the command below.

 Module       | Command  
 ------------ | -------  
 shade python | `pip install shade`

### 3. Configure Secure Channel  
Communication between the MetroÆ Host and the target servers (hypervisors) occurs via SSH. For every target server, run the following commands as the MetroÆ user on the MetroÆ server to establish a secure channel.

1. To generate SSH Keys run the following command.  
`ssh-keygen`  

2. To copy the public key to the authorized_keys file on each `target_server` run the applicable command below, replacing [target_server_username] and [target_server] with the appropriate details. 
* When working as 'root': `ssh-copy-id root@[target_server]` 
* When working as `target_server_username`: `ssh-copy-id [target_server_username]@[target_server]`  

### 4. Configure NTP sync
For proper operation Nuage components require clock synchronization with NTP. Best practice is to synchronize time on the target servers that Nuage VMs are deployed on, preferrably to the same NTP server as used by the components themselves.  

### 5. Install ovftool (for VMware only)
 If you are installing VSP components in a VMware environment (ESXi/vCenter) download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroÆ uses ovftool for OVA operations.  
 
### 6. Unzip Nuage Files
Ensure that the required unzipped Nuage software files (QCOW2, OVA, and Linux Package files) are available for the components to be installed. Use one of the two methods below.

#### Method One: Automatically
Run the command below, replacing [zipped_directory] and [nuage_unzipped_files_dir] with the actual paths:

```
./nuage-unzip.sh [zipped_directory] [nuage_unzipped_files_dir]
```
Note: After completing setup you will customize for your deployment, and you'll need to add this unzipped files directory path to `common.yml`.  

#### Method Two: Manually
Alternatively, you can create the directories under the [nuage_unzipped_files_dir] directory and manually copy the appropriate files to those locations as shown in the example below.

  ```
  <nuage_unzipped_files_dir>/vsd/qcow2/
  <nuage_unzipped_files_dir>/vsd/ova/ (for VMware)
  <nuage_unzipped_files_dir>/vsc/
  <nuage_unzipped_files_dir>/vrs/el7/
  <nuage_unzipped_files_dir>/vrs/ul16_04/
  <nuage_unzipped_files_dir>/vrs/vmware/
  <nuage_unzipped_files_dir>/vrs/hyperv/
  <nuage_unzipped_files_dir>/vstat/
  <nuage_unzipped_files_dir>/vns/nsg/
  <nuage_unzipped_files_dir>/vns/util/
  ```
Note: After completing setup you will customize for your deployment, and you'll need to add this unzipped files directory path to `common.yml`. 

## Next Step
After you've set up your environment you're ready to [customize](CUSTOMIZE.md) for your topology. 

## You May Also Be Interested in
[Encrypting Sensitive Data in MetroÆ](VAULT_ENCRYPT.md)  
[Deploying Components in AWS](AWS.md)

## Questions, Feedback, and Contributing
Ask questions and get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
You may also contact us directly.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
