# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.7.0
* Nuage Release Alignment 20.10
* Date of Release 29-September-2021

## Release Contents

### Feature Enhancements

* Predeploy NSGV without vsd license file (METROAE-497)
* Added support for hardening Elasticsearch nodes (METROAE-486)
* Allow custom configuration of RAM, CPU and Memory for VSD and VSTAT (METROAE-477)
* Run VSD Database pre-upgrade checks (METROAE-428)
* Support NFS server config using MetroAE(METROAE-557)
* Webfilter should optionally use HTTP Proxy (METROAE-493)
* Add support for encrypting credentials in Excel spreadsheet (METROAE-552)
* Add Ansible 3.4.0 support (METROAE-344)
* Allow installing/renewal of VSTAT(ES) licenses during install, upgrade and standalone (METROAE-591)

### Resolved Issues

* Check for ejabberd license expiry (METROAE-505)
* Added support install of SD-WAN portal without the SMTP address(METROAE-492)
* Fixed yum lock timeout issue when installing packages in KVM (METROAE-507)
* Replacing known_hosts module mgmt_ip to hostname (METROAE-481)
* Remove unnecessary debug lines from vsc-health (MetroAE-541)
* Fixing vsd-destroy to destroy old and new VMs (METROAE-504)
* Fix MetroAE errors while deploying using SSH Proxy (MetroAE-574)
* Fixed Check passwordless ssh from metro host to hypervisors and components ( METROAE-520)
* Added ES servers to NUH GUI ( METROAE-491)
* Fix NUH install on 20.10.R5 (METROAE-490)
* Fixing message issue for docker pull(METROAE-527)
* Install NUH optionally without DNS entry (METROAE-375)
* Add procedure for NUH copy certificates if installed before VSD(METROAE-559)
* Create NUH users and certs for NSG bootstrapping (METROAE-487)
* Enhance check to accept both access_port_name and access_ports variables being undefined (METROAE-585)
* VSTAT VSS UI should be set for all VSTATS (METROAE-580)
* Remove Old MetroAE container support (METROAE-564)
* Fix MetroAE VSD in-place upgrades for custom credentials (METROAE-586)
* Make changes into documentation for supporting ansible version upgrade(METROAE-588)
* Document where credentials are used(METROAE-532)
* Fix MetroAE inplace upgrade from 20.10.R6.1 to 20.10.R6.3(METROAE-590)
* Allow for a custom config file during VSC Upgrade (METROAE-485)
* On applying branding to the VSD jboss restart should happen serially (METROAE-597)
* Clean up temporary ISO file on VSD after mounting (METROAE-598)

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
