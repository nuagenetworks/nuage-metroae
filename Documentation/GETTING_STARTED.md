# Metro Automation Engine Quick Start Guide  

## 1. Read documentation

1.1 [Readme](../README.md) for information on supported components  
1.2 [Setup](SETUP.md) for setting up the Metro Automation Engine host and enabling SSH  
1.3 [Customize](CUSTOMIZE.md) for customizing user data and files  
1.4 [Release Notes](RELEASE_NOTES.md) for information on the latest features   

## 2. Setup Metro Automation Engine Host

#### What's a Metro Automation Engine Host?

* It can be a VM, physical server or container.
* It requires CentOS 7.x or RHEL 7.x with basic packages.
* We recommend that you dedicate a machine (VM) for it.   

2.1 Clone the master branch of the repo onto the **Metro Automation Engine Host**. Read [Setup](SETUP.md) for details.  
```
git clone https://github.com.com/nuagenetworks/nuage-metro.git
```
2.2 Install the required packages. Run as root or sudo. Read [Setup](SETUP.md) for details.  
```
$ sudo ./metro-setup.sh  
```

## 3. Enable SSH Access  

### 3.1 For Metro Automation Engine User

3.1.1 As Metro Automation Engine User, generate SSH keys: `ssh-keygen`.  
3.1.2 Copy SSH public key: `ssh-copy-id localhost`.  

### 3.2 For Root User  

3.2.1 As root user, generate SSH keys: `ssh-keygen`.  
3.2.2 Copy SSH public key: `ssh-copy-id localhost`.  

### 3.3 For Every Target Server  

3.3.1 Copy SSH public key: `ssh-copy-id root@<target_server>`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Replace `<target server>` with actual IP address of KVM hypervisor.  

See [Setup](SETUP.md) for more details about enabling SSH Access.   

## 4. Install ovftool (for VMware only)  

Download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. Metro Automation Engine uses ovftool for OVA operations.

## 5. Prepare your environment  

5.1 Unzip Nuage files: `./metro-ansible nuage_unzip`. See [CUSTOMIZE](CUSTOMIZE.md) for details.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure that Nuage packages (tar.gz) are available on localhost (Metro Automation Engine host),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;either in a native directory or NFS-mounted.  

## Checklist for Target Servers

### KVM

- [ ] Metro Automation Engine host has ability to do a password-less SSH as root.  
- [ ] Sufficient disk space / resources exist to create VMs.  
- [ ] KVM is installed.  
- [ ] All required management and data bridges are created.  

### vCenter  

- [ ] User specified in build_vars.yml has required permissions to create and configure a VM.  
- [ ] ovftool has been downloaded from VMware onto the Metro Automation Engine Host.  
- [ ] pyvmomi has been installed on Metro Automation Engine Host: `pip install pyvmomi`.

## Next Steps

Refer to the list of documents in [README.md](../README.md) for guidance on deploying, upgrading, etc.

## Questions, Feedback, and Contributing

Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage Metro Automation Engine by submitting your own code to the project.
