# MetroAE Quick Start Guide  

## 1. Read documentation

1.1 [Readme](../README.md) for information on supported components  
1.2 [Setup](SETUP.md) for setting up the MetroAE host and enabling SSH  
1.3 [Customize](CUSTOMIZE.md) for customizing user data and files  
1.4 [Release Notes](RELEASE_NOTES.md) for information on the latest features  

## 2. Setup MetroAE Host

#### What's a MetroAE Host?

* It can be a VM, physical server or container.
* It requires CentOS 7.x or RHEL 7.x with basic packages.
* We recommend that you dedicate a machine (VM) for it.  

2.1 Clone the master branch of the repo onto the **MetroAEe Host**. Read [Setup](SETUP.md) for details.  
```
git clone https://github.com/nuagenetworks/nuage-metro.git
```
2.2 Install the required packages. Run as root or sudo. Read [Setup](SETUP.md) for details.  
```
$ sudo ./setup.sh  
```

## 3. Enable SSH Access

Passwordless SSH must be configured between the MetroAE host and all target servers, a.k.a. hypervisors. This is accomplished by generating SSH keys for the MetroAE user, then copying those keys to the authorized_keys files for the `target_server_username` on every `target_server`. The following steps should be executed on the MetroAE server as the MetroAE user.

### 3.1 Generate keys for the MetroAE user

3.1.1 As MetroAE User on the MetroAE server, generate SSH keys: `ssh-keygen`

### 3.2 Copy public key to each `target_server`

#### 3.2.1 When you are going to run as 'root' on each `target_server`

As MetroAE User on the MetroAE server, copy SSH public key: `ssh-copy-id root@<target_server>`  

#### 3.2.2 When you are going to run as `target_server_username` on each `target_server`

As MetroAE User on the MetroAE server, copy SSH public key: `ssh-copy-id <target_server_username>@<target_server>`.  

See [Setup](SETUP.md) for more details about enabling SSH Access.  

## 4. Install ovftool (for VMware only)  

Download and install the [ovftool](https://www.vmware.com/support/developer/ovf/) from VMware. MetroAE uses ovftool for OVA operations. Note that MetroAE is tested using ovftool version 4.3. ovftool version 4.3 is required for proper operation.

Note that running the metroae Docker container for VMware installations and upgrades requires special handling of the location of the ovftool command. Please see [SETUP.md](SETUP.md) for details.

## 5. Prepare your environment  

### 5.1 Unzip Nuage files: `metroae tools unzip images <zipped_directory> <unzip_directory>`. See [SETUP.md](SETUP.md) for details.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Be sure that Nuage packages (tar.gz) are available on localhost (MetroAE host),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;either in a native directory or NFS-mounted.  

### 5.2 Checklist for Target Servers

#### KVM

- [ ] MetroAE host has ability to do a password-less SSH as root to the target server.  
- [ ] Sufficient disk space / resources exist to create VMs.  
- [ ] KVM is installed.  
- [ ] All required management and data bridges are created.  

#### vCenter  

- [ ] User specified has required permissions to create and configure a VM.  
- [ ] ovftool has been downloaded from VMware onto the MetroAE Host.  
- [ ] pyvmomi has been installed on MetroAE Host: `pip install pyvmomi`.

### 5.3 Reachability

MetroAE host must be able to resolve the host names of the Nuage components into their correct management IP addresses. This is required so that MetroAE can operate on each component in the deploy, post-deploy, and health workflows.

## Next Steps

Refer to the list of documents in [README.md](../README.md) for guidance on deploying, upgrading, etc.

## Questions, Feedback, and Contributing  
Get support via the [forums](https://devops.nuagenetworks.net/forums/) on the [MetroAE site](https://devops.nuagenetworks.net/).  
Ask questions and contact us directly at [devops@nuagenetworks.net](mailto:deveops@nuagenetworks.net "send email to nuage-metro project").
 
Report bugs you find and suggest new features and enhancements via the [GitHub Issues](https://github.com/nuagenetworks/nuage-metro/issues "nuage-metro issues") feature.

You may also [contribute](../CONTRIBUTING.md) to MetroAE by submitting your own code to the project.
