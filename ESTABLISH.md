# Establishing the Ansible Environment

## Prerequisites
Before you begin working with the nuage-metro project please take these requirements and restrictions into account. Also, review README.md for a list of supported VCS/VNS components, as well as supported target server types.
* Ansible 2.2.1 is required.
* The Ansible deployment host uses python-jinja2 >= 2.7. The required python-jinja2 package is installed by default with Ansible.
  Note: el6 hosts (e.g. CentOS 6.8) are limited to python-jinja2 < 2.7. Therefore, nuage-metro cannot be deployed from an el6 host.
* The hypervisor hosts must be running RedHat or CentOS. Support for Ubuntu exists, but has been deprecated.
* If host names are used for target systems, VSD, VSC, VSTAT, VNSUTIL and VRS nodes, those names must be discoverable via DNS or added to the `/etc/hosts` file of the Ansible deployment host.
* The Ansible deployment host may also be a target server.
## Setting Up the Ansible Deployment Host
### Set Up Communication Protocol
 1. Create ssh key pair for the user that runs metro playbooks  
`ssh-keygen`

 2. Copy ssh keys to localhost's authorized key file  
`ssh-copy-id localhost`
### Install Package Management System (pip) and Required Packages
 1. Install Python pip on the Ansible host based on Redhat or Debian OS families  
`yum install python2-pip apt-get install python-pip`  

 2. Install Ansible 2.2.1 on the Ansible host for full support  
`pip install ansible==2.2.1`  
 3. Install Netmiko and its dependencies on the Ansible host  
`pip install netmiko`  
 4. Install netaddr and its dependencies on the Ansible host  
`pip install netaddr`  
 5. Install ipaddress and its dependencies on the Ansible host  
`pip install ipaddress`  
 6. Install Python pexpect module on the Ansible host   
`pip install pexpect`  
 7. Install VSPK Python module on the Ansible host  
`pip install vspk`  

  #### Additional Steps for vCenter Deployments Only  
  Note: Only Nuage software version 4.0R7 and greater is supported.  

  8. Install pysphere and pyvmomi packages on the Ansible deployment host  
`pip install pysphere pyvmomi`  

  9. Install `ovftool` package on the Ansible deployment host  
 Download [VMware OVF Tool](https://www.vmware.com/support/developer/ovf/)  
 #### Additional Step for OpenStack Only  
  8. Install `shade` Python module on the Ansible deployment host  
 `pip install shade`  
### Clone the Repository
The last step for establishing the Ansible environment is to clone the `master` branch of the nuage-metro repository to the Ansible host.  
Note: The `master` branch contains the latest stable code. the `dev` branch is for ongoing development, and its stability is not guaranteed.  
## Next Steps
* If you have NOT previously deployed VSP, proceed to `BUILD.md` for instructions on Customizing the Environment and Deploying.

* If you have previously deployed VSP, and would like to upgrade to the next version, proceed to `UPGRADE.md` for instructions on Customizing the Environment and Upgrading.  

* If you have previously deployed VSP, and would like to remove the existing deployment and start over:  
 1. Ensure that `build-vars.yml` accurately represents your existing configuration.  
 2. Destroy the existing deployment with the following command:  
 `./metro-ansible destroy_everything.yml`
 3. Proceed to `BUILD.md` for instructions on Customizing the Environment and Deploying.
---
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

 You may also ask questions and get support on the [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project") mailing list.
