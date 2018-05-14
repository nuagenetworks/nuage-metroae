# MetroAG Quick Start Guide  

## 1. Read documentation
1.1 [Readme](../README.md) for information on supported components  
1.2 [Setup](SETUP.md) for setting up the MetroAG host and enabling SSH  
1.3 [Build](BUILD.md) for customizing and building the environment  
1.4 [Release Notes](RELEASE_NOTES.md) for information on the latest features   

## 2. Setup MetroAG Host
#### What's a MetroAG Host?
* It can be a VM, physical server or container.
* It requires CentOS 7.x or RHEL 7.x with basic packages.
* We recommend that you dedicate a machine (VM) for it.   

2.1 Clone the master branch of the repo onto the **MetroAG Host**. Read [Setup](SETUP.md) for details.  
```
git clone https://github.com.com/nuagenetworks/nuage-metro.git
```
2.2 Install the required packages. Run as root or sudo. Read [Setup](SETUP.md) for details.  
```
$ sudo ./metro-setup.sh  
```

## 3. Enable SSH Access  
### 3.1 For MetroAG User
3.1.1 As MetroAG User, generate SSH keys: `ssh-keygen`.  
3.1.2 Copy SSH public key: `ssh-copy-id localhost`.  
### 3.2 For Root User  
3.2.1 As root user, generate SSH keys: `ssh-keygen`.  
3.2.2 Copy SSH public key: `ssh-copy-id localhost`.  
### 3.3 For Every Target Server  
3.3.1 Copy SSH public key: `ssh-copy-id root@<target_server>`.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Replace `<target server>` with actual IP address of KVM hypervisor.  

See [Setup](SETUP.md) for more details about enabling SSH Access.   
## 4. Install ovftool (for VMware only)  
Download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroAG uses ovftool for OVA operations.

## 5. Build your environment  
5.1 Customize variables in configuration files. See [BUILD](BUILD.md) for details.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure to define `nuage_zipped_files_dir` and `nuage_unzipped_files_dir` in `build_vars.yml`.  
5.2 Unzip Nuage files: `./metro-ansible nuage_unzip.yml`. See [BUILD](BUILD.md) for details.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure that Nuage packages (tar.gz) are available on localhost (MetroAG host),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;either in a native directory or NFS-mounted.  
5.3 Execute the build playbook: `./metro-ansible build.yml`.  

## Checklist for Target Servers
### KVM
- [ ] MetroAG host has ability to do a password-less SSH as root.  
- [ ] Sufficient disk space / resources exist to create VMs.  
- [ ] KVM is installed.  
- [ ] All required management and data bridges are created.  
### vCenter  
- [ ] User specified in build_vars.yml has required permissions to create and configure a VM.  
- [ ] ovftool has been downloaded from VMware onto the MetroAG Host.  
- [ ] pyvmomi has been installed on MetroAG Host: `pip install pyvmomi`.

## Next Steps
Refer to the list of documents in [README.md](../README.md) for guidance on deploying, upgrading, etc.

## Questions, Feedback, and Contributing
Ask questions and get support via email.  
  Outside Nokia: [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project")  
  Internal Nokia: [nuage-metro-interest@list.nokia.com](mailto:nuage-metro-interest@list.nokia.com "send email to nuage-metro project")

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to Nuage MetroAG by submitting your own code to the project.
