# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.4.0
* Nuage Release Alignment 20.10
* Date of Release 14-April-2021

## Release Contents

### Feature Enhancements
* Added support for upgrading inplace VSD after the installation of VSD is finished (METRO-235)
* Add support for Encrypted plugin variables for Metroae (METROAE-372)

### Resolved Issues
* Added playbook and menu option to run security hardening on VSD after the VSD installation (METROAE-328)
* Added playbook for portal deployment, this is deployemnt in an already created VMs for portal (METROAE-273)
* Fixed NSG package Unzipped Twice (METROAE-415)
* Added ansible reset connection to fix VSC connectivity issues
* Fix openstack ssl connection error (METROAE-425)

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
