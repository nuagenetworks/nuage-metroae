# Metro: Release Notes

## Metro version
v2.2.0

# Metro assumes that user will not change the names of Nuage distributed files

## New features
1. Added VSD/VSC rollback for clustered VSD upgrades on KVM platform.
1. Added support for Standalone and Clustered VSTAT upgrade
1. Added support for deployments and upgrades to 5.0.x covering changes introduced in VSD 5.0.1 related to new VSD user
1. Added VSD license validation for upgrades across major versions (ex. 4.0.x to 5.0.1)
1. Added VNS support for Vmware platforms to deploy VNS utility vm and NSGv
1. Introduced vmname as a variable that can used to set name of the vm on kvm and vcenter
 
## Usage Notes
 
## Resolved Issues
1. VSD DB backup failure during upgrades.
1. VSD purge timer restore failure during standalone upgrades.
1. VSD decouple report path is fixed. It now logs to reports folder. 
1. Added missing command to enable stats on vsd(s) when vstat is clustered
1. Fixed technical alert 17-0506 - VSD Cluster upgrade failure due to out of memory problem
1. Remove hard coded vspk versions and use vsd version to load the vspk version dynamically 
1. Added support for setting /etc/hostname
1. Fixed issue unzipping to NFS-mounted file systems
1. Fixed issue with yum updates needing to use a proxy under certain circumstances
1. Added support to unzip VRS for VMware
1. Fixed "creates" value when deploying via heat
1. Added verification that vsd_fqdn_global is set during the build process
1. libvirtd is now started when setting up hypervisor prerequisites

## Known Issues
 
## Known Limitations
 
1. VSD health checks during the upgrade only takes in to account monit summary, not other checks.
1. No support for release specific commands to stop elastic search/vstat process on vsd.
1. No support for release specific commands to stop core process on vsd.
1. Nuage Metro will not run on el6 (e.g. CentOS 6.8) hosts due to a lack of modern python-jinja2 support.
1. VSC disconnect from VSD prior 5.0.1 upgrade is not yet implemented
1. VNS support on VMware is only available for VSP version 5.0.1 and later.
1. VSPK version in nuage_vspk.py is set to v4_0 for aws deployments of nsgv

