# Metro Automation Engine Release Notes

## Release info

* MetroAE Version 4.1.0
* Nuage Release Alignment TBD
* Date of Release TBD

## Release Contents

### Feature Enhancements

* Add support for VSTAT yum update via vstat_yum_update (METROAE-1190)
* Check hypervisor disk space on KVM and vCenter
* Add NETCONF RPMs to unzip
* Add Netconf Manager Support to MetroAE (METROAE-1204)
* Added support for Python virtual environments (METROAE-1381)
* Added file check for nsgv_bootstrap.yml and example (METROAE-1379)
* Make hostname optional for VSC
* Backup and restore functionality for VSD and VSC (METROAE-1382)
* Add support for new Nuage version format, e.g. 20.6 (METROAE-1343)
* Support NUH install when VSD is not installed (METROAE-1357)
* Add support for deploying VNS Utils on Openstack
* Added a restriction for vsc_fallocate_size_gb to 1GB and skip if the value is 0
* Add support for applying custom VSC configurations (METROAE-1328)

### Resolved Issues

* Remove redundant "vcpu" tag from KVM XML
* Enable schema format enforcement (METROAE-1378)
* Change default NUH ram to 8 GB from 4 GB (METROAE-1355)
* Upgrade pyYaml to 4.2b1 to address security vulnerability
* Fixed deployment examples to have correct variable types (METROAE-1194)
* Fixed undefined variable for nsgv-predeploy on vcenter
* Fix VCENTER upgrades using container
* Fix CPU pinning for NUH and perform NTP sync (METROAE-1397)
* Support Ejabberd license install
* Fix missing fallocate flag during vsc predeploy

## Test Matrix

This release was tested according to the following test matrix. Other combinations and versions have been tested in previous releases of MetroAE and are likely to work. We encourage you to test this in your lab before you apply it in production.

Workflow | Target Server | Version
-------- | -------- | --------
Install | KVM | Geo-redundant 6.0.3
Install | KVM | HA 5.3.3
Install | KVM | HA 5.4.1
Install | KVM | HA 6.0.3
Install | KVM | Active-Standby ES 6.0.3
Install | KVM | HA IPv6 6.0.3
Install | KVM | SA 5.3.3
Install | KVM | SA 5.4.1
Install | KVM | SA 6.0.3
Install | KVM | Add VSC pair 6.0.3
Install | KVM | SA CPU pinning 6.0.3
Install | KVM | SA VNS end-to-end 6.0.3
Install | KVM | SA VNS multi-uplinks 6.0.3
Install | KVM | SA feature tests 6.0.3
Install | KVM | SA IPv6 6.0.3
Install | KVM | SA Terraform 6.0.3
Install | KVM | SA via Container 6.0.3
Install | OpenStack | HA 5.3.2
Install | OpenStack | HA 6.0.3
Install | OpenStack | SA 5.3.2
Install | OpenStack | SA 6.0.3
Install | vCenter | HA w/VCIN 6.0.3
Install | vCenter | HA w/Hybrid VCIN 6.0.3
Install | vCenter | HA 5.3.3
Install | vCenter | HA 5.4.1
Install | vCenter | HA 6.0.3
Install | vCenter | HA Custom passwords 6.0.3
Install | vCenter | SA 5.3.3
Install | vCenter | SA 5.4.1
Install | vCenter | SA 6.0.3
Install | vCenter | SA Custom passwords 6.0.3
Upgrade | KVM | Geo-redundant 5.4.1-6.0.3
Upgrade | KVM | HA 5.3.3-6.0.3
Upgrade | KVM | HA inplace 5.4.1-5.4.1U5
Upgrade | KVM | HA 5.4.1-6.0.3
Upgrade | KVM | HA hardened 5.4.1-6.0.3
Upgrade | KVM | HA inplace 6.0.3-6.0.5
Upgrade | OpenStack | HA 5.4.1-6.0.3
Upgrade | OpenStack | SA 5.4.1-6.0.3
Upgrade | vCenter | HA 5.4.1-6.0.3
Upgrade | vCenter | HA hardened 5.4.1-6.0.3
Upgrade | vCenter | HA inplace 5.4.1-5.4.1U5
Upgrade | vCenter | HA inplace 6.0.3-6.0.5
Upgrade | vCenter | SA hardened 5.3.3-6.0.3
Upgrade | vCenter | SA 5.4.1-6.0.3
Wizard Install | KVM | SA via container 6.0.3
Wizard Install | KVM | SA via CSV 6.0.3
Wizard Upgrade | KVM | SA 5.4.1-6.0.3
