# MetroÆ Quick Start Guide  

## 1. Read documentation

1.1 [Readme](../README.md) for information on supported components  
1.2 [Setup](SETUP.md) for setting up the MetroÆ host and enabling SSH  
1.3 [Customize](CUSTOMIZE.md) for customizing user data and files  
1.4 [Release Notes](RELEASE_NOTES.md) for information on the latest features   

## 2. Setup MetroÆ Host

#### What's a MetroÆ Host?

* It can be a VM, physical server or container.
* It requires CentOS 7.x or RHEL 7.x with basic packages.
* We recommend that you dedicate a machine (VM) for it.   

2.1 Clone the master branch of the repo onto the **MetroÆe Host**. Read [Setup](SETUP.md) for details.  
```
git clone https://github.com/nuagenetworks/nuage-metro.git
```
2.2 Install the required packages. Run as root or sudo. Read [Setup](SETUP.md) for details.  
```
$ sudo ./metro-setup.sh  
```

## 3. Enable SSH Access

Passwordless SSH must be configured between the MetroÆ host and all target servers, a.k.a. hypervisors. This is accomplished by generating SSH keys for the MetroÆ user, then copying those keys to the authorized_keys files for the `target_server_username` on every `target_server`. The following steps should be executed on the MetroÆ server as the MetroÆ user.

### 3.1 Generate keys for the MetroÆ user

3.1.1 As MetroÆ User on the MetroÆ server, generate SSH keys: `ssh-keygen`

### 3.2 Copy public key to each `target_server`

#### 3.2.1 When you are going to run as 'root' on each `target_server`

As MetroÆ User on the MetroÆ server, copy SSH public key: `ssh-copy-id root@<target_server>`  

#### 3.2.2 When you are going to run as `target_server_username` on each `target_server`

As MetroÆ User on the MetroÆ server, copy SSH public key: `ssh-copy-id <target_server_username>@<target_server>`.  

See [Setup](SETUP.md) for more details about enabling SSH Access.   

## 4. Install ovftool (for VMware only)  

Download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroÆ uses ovftool for OVA operations. Note that MetroÆ is tested using ovftool version 4.3. ovftool version 4.3 is required for proper operation.

Note that running the metroae Docker container for VMware installations and upgrades requires special handling of the location of the ovftool command. Please see [SETUP.md](SETUP.md) for details.

## 5. Prepare your environment  

5.1 Unzip Nuage files: `./nuage-unzip.sh <zipped_directory> <unzip_directory>`. See [SETUP.md](SETUP.md) for details.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure that Nuage packages (tar.gz) are available on localhost (MetroÆ host),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;either in a native directory or NFS-mounted.  

## Checklist for Target Servers

### KVM

- [ ] MetroÆ host has ability to do a password-less SSH as root.  
- [ ] Sufficient disk space / resources exist to create VMs.  
- [ ] KVM is installed.  
- [ ] All required management and data bridges are created.  

### vCenter  

- [ ] User specified has required permissions to create and configure a VM.  
- [ ] ovftool has been downloaded from VMware onto the MetroÆ Host.  
- [ ] pyvmomi has been installed on MetroÆ Host: `pip install pyvmomi`.

## Next Steps

Refer to the list of documents in [README.md](../README.md) for guidance on deploying, upgrading, etc.

## Questions, Feedback, and Contributing
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroÆ site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").  

Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroÆ by submitting your own code to the project.
