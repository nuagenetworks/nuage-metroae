# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.4.0
* Nuage Release Alignment 20.10
* Date of Release 14-April-2021s

## Release Contents

### Feature Enhancements
* Fix up the image paths to root at /metroae_data/ when in the container
* Added support for bootstraping NSGv using NUH external interfaces
* Support multiple KVM bridges for NUH external interfaces
* Added multi cpu core support for NSGV (METROAE-309)
* Improve VSD security hardening to monitor service shutdown (METROAE-285)
* Add next-hop to VSC VPRN config (METROAE-319)
* Add VCIN SA upgrade support for Major Minor and Inplace Upgrade(METROAE-317)
* Adding support for sending usage back to MetroAE team
* Support for configuring NUH for stats-out proxy (METROAE-288)
* Add plugin examples and documentation to MetroAE (METROAE-354)
* Added support for instantiating and bootstrapping NSGv on AWS with VSP components deployed outside AWS (METROAE-355)

### Resolved Issues
* Enhance several license file descriptions to include the file name
* Updated SDWAN portal to support 20.11 version
* Force rebuild after missing files (METROAE-298)
* Updated SDWAN portal unzip task to copy the container tar file to correct folder
* Fixed VSD deploy task to be idempotent (METROAE-304)
* Fixed sshpass quotes for passwords that has special characters (METROAE-312)
* Add option to override VSC config (METROAE-314)
* Allow portal install without VSTAT fqdn (METROAE-301)
* Fix VSR deploy errors (METROAE-310)
* Fix vsd-install script parameters (METROAE-347)
* Fix DNS dns_mgmt and dns_data to relax requirement of having specific length. (METROAE-315)
* Add vstat-health role to vstat_health playbook (METROAE-322)
* Hide log output in vsd-node-info (METROAE-332)
* Remove vstat-vsd-health role from vstat_health playbook (METROAE-322)
* Removed extra DEBUG line from nsgv-postdeploy (METROAE-334)
* Removed DEBUG tasks which are not working in upgrade shutdown playbooks ( METROAE-358)
* Updated and Reorder Pip requirements because of pip package version changes
* Fix MetroAE setup error for setuptools install
* Allowing metroae to continue execution if the vsd_continue_on_failure is set to true (METROAE-324)
* Allowing metroae to continue execution if the vsd_continue_on_failure is set to true (METROAE-324)
* Fix webfilter install required bridges issue (METROAE-371)
* Added playbook and menu option to run security hardening on VSD after the VSD installation (METROAE-328)

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
