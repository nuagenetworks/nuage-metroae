# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.6.0
* Nuage Release Alignment 20.10
* Date of Release 16-September-2021

## Release Contents

### Feature Enhancements

* Allow custom configuration of RAM, CPU and Memory for VCenter (METROAE-433)
* Added support for extra ES disk on vmware (METROAE-341)
* Add Support for Single-Step VSD Stats-out Upgrade and Patch (METROAE-470)
* Added support for different disk provisioning type for VSD and VSTAT (METROAE-453)
* Added support for blocking iptables VSC entries during upgrade (METROAE-427)
* Add support for BGP interface for VSC (METROAE-484)
* Added support for deploying NUH in VMware - requires Ansible 2.9.7 or greater and NUH version 20.10.5 or newer (METROAE-435)
* Added documentation for starting VSD with interfaces disabled on vCenter
* Added support for multiple webfilters deployment (METROAE-458)
* Added support for mounting an extra disk on VSTAT in a VMware environment (METROAE-480)
* Added support for destroying NUH in VMware (METROAE-506)

### Resolved Issues

* Added playbook and menu option to run security hardening on VSD after the VSD installation (METROAE-328)
* Added playbook for portal deployment, this is deployemnt in an already created VMs for portal (METROAE-273)
* Fixed NSG package Unzipped Twice (METROAE-415)
* Added ansible reset connection to fix VSC connectivity issues
* Fix openstack ssl connection error (METROAE-425)
* Add option to skip disable stats collection during VSTAT Upgrade (METROAE-430)
* For VSD upgrade check for 3 tar.gz files and not 3 files
* Removed unnecessary debug lines (METROAE-455)
* Added a task to check existence of vsd migration script during upgrade (METROAE-306)
* Fixed issue with installing required libvirt libraries on target host (METROAE-447)
* VSD inplace upgrade should unmount the ISO after upgrade (METROAE-449)
* Fix stats out upgrade for hardened Stats-out VSD nodes (METROAE-450)
* Fix VSD Standby nodes inplace upgrade (METROAE-452)
* Added fix for DNS destroy uses inventory_hostname instead of vmname(METROAE-405)
* Removed nuagex support (METROAE-467)
* Apply VSD Branding only for primary VSDs(METROAE-471)
* Upgraded ansible version and packages to remove depandabot alerts (METROAE-401)
* Fixed Upgrade with Custom VSD GUI password(METROAE-454)
* Apply VSD Custom Branding for patch upgrades(METROAE-469)
* Fixed validate certs in vsd-deploy for OpenStack(METRO-464)
* Removed failure_report_path from vsc-health and group_vars/all(METROAE-483)
* Removed redundant known_hosts in vsc-health & vsd-health(METROAE-482)
* Fixed incorrect smtp.user and smtp.port specifications for portal(METROAE-496)
* Fixed VSTAT VSC health check to look for correct VSDs when using stats out configuration
* Reset vsd_sa_or_ha internal flag to sa before doing stats out VSDs upgrade
* Removed multiple standalone VSC upgrade feature (METROAE-418)
* Removed redundant checks in VSTAT health(METROAE-508)
* Allow VSD Decoupling to finish before check status(METROAE-522)
* Removed redundant debug statements in VSTAT health (METROAE-517)
* Removed redundant debug statements in vstat-destroy (METROAE-518)
* Removed redundant debug statements in vsd-services-stop (METROAE-519)

## Test Matrix

This release was tested according to the following test matrix. Other combinations and versions have been tested in previous releases of MetroAE and are likely to work. We encourage you to test MetroAE in your lab before you apply it in production.

Workflow   | Target Server   | Version
---------- | --------------- | --------------------
CONFIGURE  | GCP             | SA-20.10.R1         
CONFIGURE  | GCP             | SA-5.4.1            
CONFIGURE  | GCP             | SA-6.0.3            
INSTALL    | GCP             | GEO-20.10.R1        
INSTALL    | GCP             | HA-20.10.R1         
INSTALL    | GCP             | HA-20.10.R1-ACTIVE-STANDBY-ES
INSTALL    | GCP             | HA-20.10.R1-IPv6    
INSTALL    | GCP             | HA-20.10.R1-NO-VSC-FALLOCATE
INSTALL    | GCP             | HA-5.4.1            
INSTALL    | GCP             | HA-6.0.3            
INSTALL    | GCP             | SA-20.10.R1         
INSTALL    | GCP             | SA-20.10.R1-ACTIVE-STANDBY-ES
INSTALL    | GCP             | SA-20.10.R1-ADD-VSC
INSTALL    | GCP             | SA-20.10.R1-CONTAINER
INSTALL    | GCP             | SA-20.10.R1-CPU-CORE
INSTALL    | GCP             | SA-20.10.R1-CPU-CORES-CPU_PINNING
INSTALL    | GCP             | SA-20.10.R1-CPU_PINNING
INSTALL    | GCP             | SA-20.10.R1-E2E     
INSTALL    | GCP             | SA-20.10.R1-E2E-MUTLI-UPLINKS
INSTALL    | GCP             | SA-20.10.R1-FEATURES
INSTALL    | GCP             | SA-20.10.R1-IPV6    
INSTALL    | GCP             | SA-20.10.R1-PLUGINS
INSTALL    | GCP             | SA-20.10.R1-TERRAFORM
INSTALL    | GCP             | SA-5.4.1            
INSTALL    | GCP             | SA-6.0.3            
INSTALL    | GCP             | STATS-OUT-20.10.R1  
INSTALL    | OPENSTACK       | HA-20.10.R1         
INSTALL    | OPENSTACK       | HA-6.0.3            
INSTALL    | OPENSTACK       | SA-20.10.R1         
INSTALL    | OPENSTACK       | SA-6.0.3            
INSTALL    | OPENSTACK       | SA-CONTAINER-6.0.3  
INSTALL    | VCENTER         | 20.10.R1-HYBRID-VCIN
INSTALL    | VCENTER         | HA-20.10.R1         
INSTALL    | VCENTER         | HA-20.10.R1-CHANGE-VSDPASS
INSTALL    | VCENTER         | HA-20.10.R1-VCIN    
INSTALL    | VCENTER         | HA-5.4.1            
INSTALL    | VCENTER         | HA-6.0.3            
INSTALL    | VCENTER         | SA-20.10.R1         
INSTALL    | VCENTER         | SA-20.10.R1-CHANGE-VSDPASS
INSTALL    | VCENTER         | SA-20.10.R1-VENV    
INSTALL    | VCENTER         | SA-5.4.1            
INSTALL    | VCENTER         | SA-6.0.3            
RESTORE    | GCP             | HA-6.0.3            
RESTORE    | GCP             | SA-6.0.3            
UPGRADE    | GCP             | GEO-5.4.1-6.0.3     
UPGRADE    | GCP             | GEO-6.0.3-20.10.R1  
UPGRADE    | GCP             | GEO-6.0.3-6.0.7-INPLACE
UPGRADE    | GCP             | HA-5.4.1-5.4.1U5-INPLACE
UPGRADE    | GCP             | HA-5.4.1-6.0.3      
UPGRADE    | GCP             | HA-5.4.1-6.0.3-HARDENED
UPGRADE    | GCP             | HA-6.0.3-20.10.R1   
UPGRADE    | GCP             | HA-6.0.3-20.10.R1-HARDENED
UPGRADE    | GCP             | HA-6.0.3-6.0.7-INPLACE
UPGRADE    | GCP             | SA-5.4.1-6.0.3      
UPGRADE    | GCP             | SA-5.4.1-6.0.3-HARDENED
UPGRADE    | GCP             | SA-5.4.1-6.0.3-VSD-SECURITY
UPGRADE    | GCP             | SA-6.0.3-20.10.R1   
UPGRADE    | GCP             | SA-6.0.3-6.0.7-INPLACE
UPGRADE    | OPENSTACK       | HA-5.4.1-6.0.3      
UPGRADE    | OPENSTACK       | SA-5.4.1-6.0.3      
UPGRADE    | VCENTER         | HA-5.4.1-6.0.3      
UPGRADE    | VCENTER         | HA-5.4.1-6.0.3-HARDENED
UPGRADE    | VCENTER         | HA-6.0.3-20.10.R1   
UPGRADE    | VCENTER         | HA-6.0.3-20.10.R1-HARDENED
UPGRADE    | VCENTER         | HA-INPLACE-5.4.1-5.4.1U5
UPGRADE    | VCENTER         | HA-INPLACE-6.0.3-6.0.7
UPGRADE    | VCENTER         | SA-5.4.1-6.0.3      
UPGRADE    | VCENTER         | SA-5.4.1-6.0.3-CONTAINER
UPGRADE    | VCENTER         | SA-6.0.3-20.10.R1   
UPGRADE    | VCENTER         | SA-6.0.3-20.10.R1-HARDENED
