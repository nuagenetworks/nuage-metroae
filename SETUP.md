# Setting Up the Nuage MetroAG Ansible Environment
## Introduction
This document describes how to setup a Nuage MetroAG environment for the purpose of deploying and upgrading Nuage Networks software. It guides you through the following areas:
* Setting up the Ansible deployment host that will run the Ansible playbooks.
* Configuring the Ansible deployment host for the user that will run the Nuage MetroAG playbooks. This user will be referred to in this document as *the installation user*.
* Setting up target servers (a.k.a. hypervisors) that will act as hosts for VSD, VSC, and other VMs.
* Setting up compute nodes that will have VRS deployed on them.
## Prerequisites
Before you begin working with the nuage-metro project please take these requirements and restrictions into account. Also, review README.md for a list of supported VCS/VNS components, as well as supported target server types.
* Ansible 2.2.1 is required.
* The Ansible deployment host must run el7 Linux host, e.g. CentOS 7.\* or RHEL 7.\*. Ansible 2.2.1 depends on a Python package that is not available on el6 Linux.  
Note: Modern Ubuntu versions, such as 14.04 and 16.04, may also work as Ansible deployment hosts, but they have not been tested.
* If host names are used for target systems, VSD, VSC, VSTAT, VNSUTIL and VRS nodes, those names must be discoverable via DNS or added to the `/etc/hosts` file of the Ansible deployment host.
* The Ansible deployment host may also be a target server.
## Setting Up the Ansible Deployment Host
### Set Up Passwordless ssh for the Installation User
 1. If not already present, create a ssh key pair for the installation user on the Ansible deployment host as follows:  
   1A. Login to the Ansible deployment host as the installation user.  
   1B. Execute the command:  `ssh-keygen`  
   1C. Follow the prompts to complete creation. It is normal to accept all defaults.
 2. Copy the ssh public key to the installation user's `authorized_keys` file. Have the file copied automatically as follows:
   2A. Login to the Ansible deployment host as the installation user.  
   2B. Execute the command: `ssh-copy-id hostname`, where *hostname* is the name of the Ansible deployment host.  
   2C. Enter the user's password if prompted.
### Install Packages Required on the Ansible Deployment host
 1. Install Python pip  
    * on RedHat OS family distributions: `yum install python2-pip`  
    * on Debian OS family distributions: `apt-get install python-pip`    
 2. Install Ansible 2.2.1 for full support  
`pip install ansible==2.2.1`  
 3. Install Netmiko and its dependencies  
`pip install netmiko`  
 4. Install netaddr and its dependencies  
`pip install netaddr`  
 5. Install ipaddress and its dependencies  
`pip install ipaddress`  
 6. Install Python pexpect module   
`pip install pexpect`  
 7. Install VSPK Python module  
`pip install vspk`  

  #### Additional Steps for vCenter Deployments Only  
  Note: vCenter deployments are supported for Nuage software version 4.0R7 and greater.  

  8. Install pysphere and pyvmomi packages on the Ansible deployment host  
`pip install pysphere pyvmomi`  

  9. Install `ovftool` package on the Ansible deployment host  
 Download [VMware OVF Tool](https://www.vmware.com/support/developer/ovf/)  
 #### Additional Step for OpenStack Only  
  8. Install `shade` Python module on the Ansible deployment host  
 `pip install shade`  
### Clone Nuage MetroAG
The last step for setting up the Nuage MetroAG environment is to put a copy of the Nuage MetroAG repository on the Ansible deployment host. Nuage MetroAG is available on GitHub.com at https://github.com/nuagenetworks/nuage-metro. From the web site you can download a zip of the archive. Or you can execute a `git clone` on your Ansible deployment host. (git will need to be installed first...)  
## Next Steps
* If you would like to deploy Nuage software components for the first time or add new components to an existing deployment, proceed to `BUILD.md` for instructions on customizing the environment and deploying.

* If you would like to upgrade existing Nuage software components to a newer version, proceed to `UPGRADE.md` for instructions on customizing the environment and upgrading.  

* If you have previously deployed VSP, and would like to remove it and start over, proceed to `DESTROY.md` for instructions on removing an existing deployment.  
---
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
