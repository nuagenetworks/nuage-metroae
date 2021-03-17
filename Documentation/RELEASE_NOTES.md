# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.4.0
* Nuage Release Alignment TBD
* Date of Release TBD

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

### Resolved Issues
* Enhance several license file descriptions to include the file name
* Updated SDWAN portal to support 20.11 version
* Force rebuild after missing files (METROAE-298)
* Updated SDWAN portal unzip task to copy the container tar file to correct folder
* Fixed VSD deploy task to be idempotent (METROAE-304)
* Fixed sshpass quotes for passwords that has special characters (METROAE-312)
* Add option to override VSC config (METROAE-314)
* Fix VSR deploy errors (METROAE-310)
* Fix DNS dns_mgmt and dns_data to relax requirement of having specific length. (METROAE-315)
* Add vstat-health role to vstat_health playbook (METROAE-322)
* Remove vstat-vsd-health role from vstat_health playbook (METROAE-322)

## Test Matrix

This release was tested according to the following test matrix. Other combinations and versions have been tested in previous releases of MetroAE and are likely to work. We encourage you to test this in your lab before you apply it in production.

Workflow | Target Server | Version
-------- | -------- | --------
Install | KVM | Geo-redundant 20.10.R1
Install | KVM | HA 5.4.1
Install | KVM | HA 6.0.3
Install | KVM | HA 20.10.R1
Install | KVM | Active-Standby ES 20.10.R1
Install | KVM | HA IPv6 20.10.R1
Install | KVM | SA 5.4.1
Install | KVM | SA 6.0.3
Install | KVM | SA 20.10.R1
Install | KVM | Add VSC pair 20.10.R1
Install | KVM | SA CPU pinning 20.10.R1
Install | KVM | SA VNS end-to-end 20.10.R1
Install | KVM | SA VNS multi-uplinks 20.10.R1
Install | KVM | SA feature tests 20.10.R1
Install | KVM | SA IPv6 20.10.R1
Install | KVM | SA Terraform 20.10.R1
Install | KVM | SA via Container 20.10.R1
Install | OpenStack | HA 5.3.2
Install | OpenStack | HA 20.10.R1
Install | OpenStack | SA 5.3.2
Install | OpenStack | SA 20.10.R1
Install | vCenter | HA w/VCIN 20.10.R1
Install | vCenter | HA w/Hybrid VCIN 20.10.R1
Install | vCenter | HA 5.4.1
Install | vCenter | HA 6.0.3
Install | vCenter | HA 20.10.R1
Install | vCenter | HA Custom passwords 20.10.R1
Install | vCenter | SA 5.4.1
Install | vCenter | SA 6.0.3
Install | vCenter | SA 20.10.R1
Install | vCenter | SA Custom passwords 20.10.R1
Upgrade | KVM | Geo-redundant 6.0.3-20.10.R1
Upgrade | KVM | HA 5.4.1-6.0.3
Upgrade | KVM | HA inplace 6.0.3-6.0.5
Upgrade | KVM | HA 6.0.3-20.10.R1
Upgrade | KVM | HA hardened 6.0.3-20.10.R1
Upgrade | KVM | HA inplace 20.10.R1-20.10.R2
Upgrade | OpenStack | HA 6.0.3-20.10.R1
Upgrade | OpenStack | SA 6.0.3-20.10.R1
Upgrade | vCenter | HA 6.0.3-20.10.R1
Upgrade | vCenter | HA hardened 6.0.3-20.10.R1
Upgrade | vCenter | HA inplace 6.0.3-6.0.5
Upgrade | vCenter | HA inplace 20.10.R1-20.10.R2
Upgrade | vCenter | SA hardened 6.0.3-20.10.R1
Upgrade | vCenter | SA 6.0.3-20.10.R1
Wizard Install | KVM | SA via container 20.10.R1
Wizard Install | KVM | SA via CSV 20.10.R1
Wizard Upgrade | KVM | SA 6.0.3-20.10.R1
